import json
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

unique_links = None 
with open('./unique_sitemap_links.json', 'r') as file:
    unique_links = set(json.load(file))

html_links = []
for link in unique_links:
    if ".pdf" not in link:
        html_links.append(link)

with open('./unique_sitemap_links.json', 'w') as file:
    json.dump(html_links, file)

new_links_not_in_sitemap = {}
for link in html_links[:10000]:
    try:
        response = requests.get(link)
        soup = bs(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        for tag in a_tags:
            if "href" in tag.attrs:
                temp_link = tag['href']

                # Construct absolute URL
                absolute_url = urljoin(link, temp_link)  # This automatically handles relative URLs

                if absolute_url not in unique_links:
                    unique_links.add(absolute_url)  # Add to set
                    if link not in new_links_not_in_sitemap:
                        new_links_not_in_sitemap[link] = []
                    # checking if the link is within company.net/documentation/en_US and it is not a page navigation link
                    if "company.net/documentation/en_US" in absolute_url and "#" not in temp_link:
                        new_links_not_in_sitemap[link].append(absolute_url)
                        print(f"{temp_link} is added to html links, which was not in unique links")
    except Exception as e:
        print(f"Failed to process {link}: {str(e)}")
    
with open('./new_links_not_in_sitemap.json', 'w') as file:
    json.dump(new_links_not_in_sitemap, file)

# count
count = 0
for key in new_links_not_in_sitemap:
    count += len(new_links_not_in_sitemap[key])
print("Count of links not in sitemap", count)
