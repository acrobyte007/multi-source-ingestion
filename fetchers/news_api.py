from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
load_dotenv()

news_client = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def fetch_news(topic_name: str, language: str = "en", num_articles: int = 1):
    articles = news_client.get_everything(
        q=topic_name,
        language=language
    )

    result = {}
    for i, article in enumerate(articles["articles"], start=1):
        result[i] = {
            "title": article.get("title"),
            "content": article.get("content") or article.get("description"),
            "source":"newsapi",
            "url": article.get("url"),
            "fetched_at":datetime.now(timezone.utc).isoformat()
        }

    return result

print(fetch_news("artificial intelligence", "en", num_articles=2))
