import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from fetchers.csv_reader import extract_csv_data_as_flat_json
from fetchers.news_api import fetch_news
from fetchers.web_scraper import scrape_page_as_title_and_content


def fetch_all_sources(url: str, csv_path: str, news_query: str, number_of_news: int,news_language: str="en"):
    # csv_data = extract_csv_data_as_flat_json(csv_path)

    news_data = fetch_news(news_query,news_language, number_of_news)
    web_data = scrape_page_as_title_and_content(url)

    def get_top_level_dicts(d):
        return {k: v for k, v in d.items() if isinstance(v, dict)}

    # csv_dicts = get_top_level_dicts(csv_data)
    news_dicts = get_top_level_dicts(news_data)

    # Combine them
    combined_data = {}
    # combined_data.update(csv_dicts)
    combined_data.update(news_dicts)
    combined_data.update(web_data)
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print("Saved combined data to articles.json")


if __name__ == "__main__":
    url = "https://docs.sqlalchemy.org/en/20/"
    csv_path = "ETL\multi-source-ingestion\Articles.csv"
    news_query = "AI"
    number_of_news = 2
    news_language = "en"

    data = fetch_all_sources(url, csv_path, news_query, number_of_news,news_language)