import json
links = None
with open("./unique_sitemap_links.json","r") as file:
    links = json.load(file)
    
# length of corpus
print(len(links))

# extension_map
file_extensions = {}
for link in links:
    extension = link.split(".")[-1]
    file_extensions[extension] = file_extensions.get(extension,0) + 1

with open('unique_file_extensions.json', 'w') as file:
    file.write(json.dumps(file_extensions))
    

pdfs = []
for link in links:
    if "pdf" in link:
        pdfs.append(link)

with open('unique_pdf_links.json', 'w') as file:
    file.write(json.dumps(pdfs))
