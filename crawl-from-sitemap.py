import requests
from bs4 import BeautifulSoup as bs
import json

BASE_URL="https://www.company.net/documentation/sitemap/sitemap.xml"

session = requests.sessions.Session()

request = session.get(BASE_URL)
soup = bs(request.content,"lxml")

sub_sitemaps = soup.findAll("loc")
engish_submaps = []
for sub in sub_sitemaps:
    if "/us/en" in sub.get_text():
        engish_submaps.append(sub.get_text().strip())
unique_documentation_links = set()
for submap in engish_submaps:
    print(f"for {submap}")
    request = session.get(submap)
    soup = bs(request.content,"lxml")
    pages= soup.findAll("loc")
    for page in pages:
        unique_documentation_links.add(page.get_text().strip())
        
print(f"{len(unique_documentation_links)} links found")

with open('unique_sitemap_links.json', 'w') as file:
    file.write(json.dumps(list(unique_documentation_links)))
