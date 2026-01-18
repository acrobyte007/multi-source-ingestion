import csv
import json
import os
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def extract_column_names_as_json(csv_file_path: str) -> dict:
    csv_file_path = os.path.normpath(csv_file_path)
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    with open(csv_file_path, newline="", encoding="cp1252") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")

        return {
            "columns": [col.strip() for col in reader.fieldnames if col and col.strip()]
        }


class NewsColumns(BaseModel):
    title: Optional[str] = Field(
        None, description="Column name best suited to be used as news title"
    )
    content: Optional[str] = Field(
        None, description="Column name best suited to be used as news article content/body"
    )

    @validator("title", "content")
    def strip_values(cls, v):
        if v:
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
Your task is to identify:

1. The column that best represents a news article title.
2. The column that best represents the main news content or body.

Rules:
- Choose only from the given column names.
- Prefer concise text fields for titles (e.g., headline, title, subject).
- Prefer long text fields for content (e.g., content, body, description, article, text).
- If no suitable column exists, return null.
- Do not hallucinate column names.

Column names:
{column_names}
"""
)


def heuristic_fallback(columns: List[str]):
    title_keywords = ["title", "headline", "subject", "heading", "news_title"]
    content_keywords = ["content", "body", "description", "article", "text", "story"]

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
    column_data = extract_column_names_as_json(csv_file_path)
    column_names = column_data["columns"]

    response = mistral_model.invoke(
        prompt.format_messages(column_names=json.dumps(column_data, indent=2))
    )

    title_col = response.title
    content_col = response.content

    # Fallback to heuristic if LLM returns nothing
    if not title_col or not content_col:
        fallback_title, fallback_content = heuristic_fallback(column_names)
        title_col = title_col or fallback_title
        content_col = content_col or fallback_content

    return {
        "title_column": title_col,
        "content_column": content_col,
        "all_columns": column_names
    }


if __name__ == "__main__":
    csv_file_path = "E:/ETL/multi-source-ingestion/Articles.csv"
    result = get_csv_column_names(csv_file_path)

    print(json.dumps(result, indent=4, ensure_ascii=False))
