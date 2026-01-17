from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
load_dotenv()
news_client=NewsApiClient(api_key=os.getenv("NEWSAPI_API_KEY"))
