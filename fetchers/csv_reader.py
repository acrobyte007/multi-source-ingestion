import csv
import json
import os
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import time
load_dotenv()


def extract_column_names(csv_file_path: str) -> List[str]:
    csv_file_path = os.path.normpath(csv_file_path)
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    with open(csv_file_path, newline="", encoding="cp1252") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")
        return [col.strip() for col in reader.fieldnames if col and col.strip()]


class NewsColumns(BaseModel):
    title: Optional[str] = Field(
        None, description="Column name best suited to be used as news title"
    )
    content: Optional[str] = Field(
        None, description="Column name best suited to be used as news article content/body"
    )

    @field_validator("title", "content", mode="before")
    @classmethod
    def strip_values(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


mistral_primary = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0,
    max_retries=2,
)

mistral_model = mistral_primary.with_structured_output(NewsColumns)

prompt = ChatPromptTemplate.from_template(
    """
You are given a list of CSV column names. 
Identify:
1. The column that best represents a news article title.
2. The column that best represents the main news content or body.

Rules:
- Choose only from the given column names.
- Prefer concise text fields for titles (e.g., title, heading, headline).
- Prefer long text fields for content (e.g., content, body, article, description).
- If no suitable column exists, return null.
- Do not invent column names.

Column names:
{column_names}
"""
)


def heuristic_fallback(columns: List[str]):
    title_keywords = ["title", "headline", "heading", "subject"]
    content_keywords = ["content", "body", "article", "description", "text", "story"]

    title_col = None
    content_col = None

    for col in columns:
        lc = col.lower()
        if not title_col and any(k in lc for k in title_keywords):
            title_col = col
        if not content_col and any(k in lc for k in content_keywords):
            content_col = col

    return title_col, content_col


def get_csv_column_names(csv_file_path: str):
    columns = extract_column_names(csv_file_path)

    response = mistral_model.invoke(
        prompt.format_messages(column_names=json.dumps(columns, indent=2))
    )

    title_col = response.title
    content_col = response.content

    if not title_col or not content_col:
        fallback_title, fallback_content = heuristic_fallback(columns)
        title_col = title_col or fallback_title
        content_col = content_col or fallback_content

    return {
        "title_column": title_col,
        "content_column": content_col
    }


def extract_csv_data_as_nested_json(csv_file_path: str, title_column: str, content_column: str):
    csv_file_path = os.path.normpath(csv_file_path)

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    results = []

    with open(csv_file_path, newline="", encoding="cp1252") as file:
        reader = csv.DictReader(file)

        if title_column not in reader.fieldnames or content_column not in reader.fieldnames:
            raise ValueError("Provided column names do not exist in the CSV file")

        for row in reader:
            title_value = row.get(title_column)
            content_value = row.get(content_column)

            if title_value and content_value:
                results.append({
                    "title": title_value.strip(),
                    "content": content_value.strip(),
                    "source": "csv",
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "url": "N/A"
                })

    return results


def extract_csv_data_as_flat_json(csv_file_path: str):
    column_json= get_csv_column_names(csv_file_path)
    title_column = column_json.get("title_column")
    content_column = column_json.get("content_column")

    return extract_csv_data_as_nested_json(csv_file_path, title_column, content_column)

if __name__ == "__main__":
    csv_path = "E:\ETL\multi-source-ingestion\Articles.csv"
    data = extract_csv_data_as_flat_json(
        csv_path
    )
    print(json.dumps(data, indent=4, ensure_ascii=False))