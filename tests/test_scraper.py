import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fetchers.web_scraper import scrape_page_as_title_and_content

def test_scrape_page_as_title_and_content():
    url = "https://docs.sqlalchemy.org/en/20/"
    result = scrape_page_as_title_and_content(url)

    # Basic structure checks
    assert isinstance(result, dict)
    assert "title" in result
    assert "content" in result
    assert "source" in result
    assert "url" in result
    assert "fetched_at" in result

    # Type checks
    assert isinstance(result["title"], str)
    assert isinstance(result["content"], str)
    assert isinstance(result["source"], str)
    assert isinstance(result["url"], str)
    assert isinstance(result["fetched_at"], str)

    # Content sanity checks
    assert len(result["title"]) > 0
    assert len(result["content"]) > 0
    assert result["source"] == "web_scraper"
    assert result["url"] == url
    assert len(result["fetched_at"]) > 0
    assert "(" in result["content"] and ")" in result["content"]
