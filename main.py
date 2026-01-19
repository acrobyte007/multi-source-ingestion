import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from fetchers.csv_reader import extract_csv_data_as_flat_json
from fetchers.news_api import fetch_news
from fetchers.web_scraper import scrape_page_as_title_and_content


def fetch_all_sources(url: str, csv_path: str, news_query: str, number_of_news: int,news_language: str="en"):
    csv_data = extract_csv_data_as_flat_json(csv_path)

    news_data = fetch_news(news_query,news_language, number_of_news)
    web_data = scrape_page_as_title_and_content(url)
    combined_data = []
    if isinstance(csv_data, list):
        combined_data.extend(csv_data)

    if isinstance(news_data, list):
        combined_data.extend(news_data)
    if isinstance(web_data, dict):
        combined_data.append(web_data)
    output_dir = r"E:\ETL\multi-source-ingestion\output"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "articles.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print(f"Saved combined data to {output_file}")
if __name__ == "__main__":
    url = "https://docs.sqlalchemy.org/en/20/"
    csv_path = "E:\ETL\multi-source-ingestion\Articles.csv"
    news_query = "AI"
    number_of_news = 2
    news_language = "en"

    data = fetch_all_sources(url, csv_path, news_query, number_of_news,news_language)