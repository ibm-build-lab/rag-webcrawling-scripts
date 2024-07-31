import json
import pandas as pd

with open("./combined_data.json","r") as file:
    data = json.load(file)

unique_sitemap_links = []

for obj in data:
    unique_sitemap_links.append(obj["link"])

len(unique_sitemap_links)

sitemap_links_set = set(unique_sitemap_links)

df = pd.read_csv("./missing_links.csv")

# df.head()
links = df["Links missing"].to_list()

missing_links  =[]
for link in links:
    if link not in unique_sitemap_links:
        missing_links.append(link)

len(missing_links)

with open("./missing_links.json","w") as file:
    json.dump(missing_links,file)
