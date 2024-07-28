from get_documentation_page_data import fetch_data
import json
from urllib.parse import urlparse, unquote
import concurrent.futures

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

def fetch_and_store_data(idx,link):
    # filename = generate_filename_from_url(link)
    print(idx,link)
    data = fetch_data(url=link,wait_per_page=5)
    return data

with open("./unique_sitemap_links.json","r") as file:
    links = json.load(file)
full_data  =[]  
# Limit the number of threads to a sensible value to avoid overwhelming the server
MAX_THREADS = 15

# Use ThreadPoolExecutor to manage threads
# soup.find("body").get_text()
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    # Submit tasks to the executor for each link
    future_to_data = {executor.submit(fetch_and_store_data, idx,link): (idx,link) for (idx,link) in enumerate(links[:100])}

    # As each thread completes, collect its result and append to full_data
    for future in concurrent.futures.as_completed(future_to_data):
        data = future.result()
        full_data.append(data)


with open("./page_data/full_data_multithreaded_100.json","w") as file:
    json.dump(full_data,file)
