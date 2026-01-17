import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def scrape_headers_with_content_and_links_as_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    def clean_text(text):
        text = text.strip()
        text = " ".join(text.split())
        return text

    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    nested_json = defaultdict(list)

    for header in headers:
        header_type = header.name
        header_level = int(header.name[1])
        header_text = clean_text(header.get_text())

        content = []

        for sibling in header.next_siblings:
            if sibling.name and sibling.name.startswith("h"):
                if int(sibling.name[1]) <= header_level:
                    break

            if sibling.name in ["p", "li", "span", "div"]:
                for a in sibling.find_all("a", href=True):
                    link_text = clean_text(a.get_text())
                    link_url = a["href"]
                    content.append(f"{link_text} ({link_url})")

                text = clean_text(sibling.get_text())
                if text:
                    content.append(text)

        nested_json[header_type].append({
            "header": header_text,
            "content": content
        })

    return dict(nested_json)


import json

url = "https://docs.sqlalchemy.org/en/20/"
data = scrape_headers_with_content_and_links_as_text(url)

print(json.dumps(data, indent=4))
