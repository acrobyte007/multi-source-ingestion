import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fetchers.news_api import fetch_news

def test_fetch_news():
    result = fetch_news("technology", "en", 1)

    # Basic structure checks
    assert isinstance(result, dict)
    assert len(result) == 1
    assert 1 in result

    article = result[1]

    # Required fields
    assert "title" in article
    assert "content" in article
    assert "url" in article
    assert "source" in article
    assert "fetched_at" in article

    # Type checks
    assert isinstance(article["title"], (str, type(None)))
    assert isinstance(article["content"], (str, type(None)))
    assert isinstance(article["url"], (str, type(None)))
    assert isinstance(article["source"], (str, type(None)))
    assert isinstance(article["fetched_at"], str)
