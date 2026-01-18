import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timezone

def scrape_page_as_title_and_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    def clean_text(text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    if not headers:
        return {"title": "", "content": ""}

    title = clean_text(headers[0].get_text())

    content_parts = []

    for header in headers:
        header_level = int(header.name[1])

        for sibling in header.next_siblings:
            if sibling.name and sibling.name.startswith("h"):
                if int(sibling.name[1]) <= header_level:
                    break

            if sibling.name in ["p", "li", "span", "div"]:
                for a in sibling.find_all("a", href=True):
                    link_text = clean_text(a.get_text())
                    link_url = a["href"]
                    content_parts.append(f"{link_text} ({link_url})")

                text = clean_text(sibling.get_text())
                if text:
                    content_parts.append(text)

    content = " ".join(dict.fromkeys(content_parts))

    return {
        "title": title,
        "content": content,
        "source": "web_scraper",
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }


url = "https://docs.sqlalchemy.org/en/20/"
data = scrape_page_as_title_and_content(url)

print(json.dumps(data, indent=4, ensure_ascii=False))
