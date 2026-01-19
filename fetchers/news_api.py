import os
import re
import time
from html import unescape
from datetime import datetime, timezone
from newsapi import NewsApiClient
from dotenv import load_dotenv
from newsapi.newsapi_exception import NewsAPIException

load_dotenv()

news_client = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def clean_content(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\[\+\d+\schars\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def fetch_news(topic_name: str, language: str = "en", num_articles: int = 2, retries: int = 3, delay: int = 2):
    attempt = 0
    while attempt < retries:
        try:
            articles = news_client.get_everything(
                q=topic_name,
                language=language,
                page_size=num_articles,
                sort_by="publishedAt"
            )

            result =[]
            for i, article in enumerate(articles["articles"], start=1):
                result.append ({
                    "title": clean_content(article.get("title")),
                    "content": clean_content(article.get("content")),
                    "source": "newsapi",
                    "url": article.get("url"),
                    "fetched_at": datetime.now(timezone.utc).isoformat()
                })

            return result

        except NewsAPIException as e:
            attempt += 1
            if attempt >= retries:
                raise RuntimeError(f"NewsAPI error after {retries} attempts: {str(e)}")
            time.sleep(delay)

        except Exception as e:
            attempt += 1
            if attempt >= retries:
                raise RuntimeError(f"Unexpected error after {retries} attempts: {str(e)}")
            time.sleep(delay)

print(fetch_news("artificial intelligence", "en", num_articles=2))
