import requests
from bs4 import BeautifulSoup
import re
import json
import time

def scrape_page_as_title_and_content(url, retries=3, delay=5):
    def clean_text(text):
        return re.sub(r'\s+', ' ', text).strip()

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException:
            if attempt < retries:
                time.sleep(delay)
            else:
                return {"title": "", "content": ""}

    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    if not headers:
        return {"title": "", "content": ""}

    title = clean_text(headers[0].get_text())
    content_parts = []

    for header in headers:
        header_level = int(header.name[1])
        for sibling in header.next_siblings:
            if sibling.name and sibling.name.startswith("h") and int(sibling.name[1]) <= header_level:
                break
            if sibling.name in ["p", "li", "span", "div"]:
                for a in sibling.find_all("a", href=True):
                    content_parts.append(f"{clean_text(a.get_text())} ({a['href']})")
                text = clean_text(sibling.get_text())
                if text:
                    content_parts.append(text)

    content = " ".join(dict.fromkeys(content_parts))
    return {"title": title, "content": content, "source": "web_scraper", "url": url, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

url = "https://docs.sqlalchemy.org/en/20/"
data = scrape_page_as_title_and_content(url)
print(json.dumps(data, indent=4, ensure_ascii=False))
