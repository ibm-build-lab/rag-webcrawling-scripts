from get_documentation_page_data import fetch_data
import json
from urllib.parse import urlparse, unquote
import concurrent.futures
import sqlite3
import jsonlines  # For working with JSONL format

def create_table():
    connection = sqlite3.connect('company_website_documentation.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            data TEXT
        )
    ''')
    connection.commit()
    connection.close()
# Function to insert data into SQL database
def insert_into_db(url, data):
    connection = sqlite3.connect('company_website_documentation.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO data_table (url, data) VALUES (?, ?)', (url, json.dumps(data)))
    connection.commit()
    connection.close()

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
    insert_into_db(link, data) 
    return data

# creating table
create_table()

with open("./unique_sitemap_links.json","r") as file:
    links = json.load(file)
full_data  =[]  
# Limit the number of threads to a sensible value to avoid overwhelming the server
MAX_THREADS = 15

# Use ThreadPoolExecutor to manage threads
# soup.find("body").get_text()
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks to the executor for each link
    future_to_data = {executor.submit(fetch_and_store_data, idx,link): (idx,link) for (idx,link) in enumerate(links)}

    # As each thread completes, collect its result and append to full_data
    for future in concurrent.futures.as_completed(future_to_data):
        data = future.result()
        # full_data.append(data)
        with jsonlines.open("./page_data/full_data_multithreaded_updated.jsonl", mode='a') as writer:
            writer.write(data)

# with open("./page_data/full_data_multithreaded_1000.json","w") as file:
#     json.dump(full_data,file)
