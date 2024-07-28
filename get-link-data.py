from get_documentation_page_data import fetch_data
import json
from urllib.parse import urlparse, unquote

def generate_filename_from_url(url):
    # Parse the URL to get the path component
    path = urlparse(url).path
    
    # Unquote URL-encoded characters
    path = unquote(path)
    
    # Split the path into segments and filter out empty segments
    segments = [segment for segment in path.split('/') if segment]
    
    # Use the last few segments of the path to form a filename
    filename = '-'.join(segments)  
    
    # Append a file extension, e.g., .html
    filename += '.json'
    
    return filename

with open("./unique_sitemap_links.json","r") as file:
    links = json.load(file)
full_data  =[]  
for idx,link in enumerate(links[:100]):
    filename = generate_filename_from_url(link)
    print(idx,link)
    data = fetch_data(url = link)
    full_data.append(data)

with open("./page_data/full_data_100.json","w") as file:
    json.dump(full_data,file)
