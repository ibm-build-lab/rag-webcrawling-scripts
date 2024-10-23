# This script crawls a website and writes into an ElasticSearch index
#
# Invoke it as: 
#
# curl -X POST http://localhost:5000/crawl -H "Content-Type: application/json" -d '{"url": "https://example.com", "index_name": "web_crawl_index"}'
#
# Search contents:
#
# curl "http://localhost:5000/search?q=example&index_name=web_crawl_index"
#
# Example resulting document in Elasticsearch:
#
# {
#   "url": "https://example.com",
#   "content": "Text content from paragraphs...",
#   "tables": [
#     {
#       "headers": ["Name", "Age", "Occupation"],
#       "rows": [
#         ["John Doe", "30", "Engineer"],
#         ["Jane Smith", "25", "Designer"]
#       ]
#     }
#   ]
# }
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Initialize Elasticsearch client
es = Elasticsearch('your-elasticsearch-uri', 
    basic_auth=('your-user', 'your-password')
)

# Create an index in Elasticsearch
def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

# Crawl the website and return the content and tables
def crawl_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content
        text_content = ' '.join([p.get_text() for p in soup.find_all('p')])

        # Extract tables
        tables = []
        for table in soup.find_all('table'):
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append({"headers": headers, "rows": rows})

        return text_content, tables
    except requests.exceptions.RequestException as e:
        return f"Error crawling the website: {e}", []

# Store crawled data in Elasticsearch
def store_in_elasticsearch(index_name, url, content, tables):
    document = {
        'url': url,
        'content': content,
        'tables': tables
    }
    es.index(index=index_name, document=document)

@app.route('/crawl', methods=['POST'])
def crawl_and_store():
    data = request.get_json()
    url = data.get('url')
    index_name = data.get('index_name', 'web_crawl_index')  # Default index name

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Crawl the website
    content, tables = crawl_website(url)
    
    if 'Error' in content:
        return jsonify({"error": content}), 500

    # Create an Elasticsearch index (if not exists)
    create_index(index_name)

    # Store the crawled content and tables in Elasticsearch
    store_in_elasticsearch(index_name, url, content, tables)

    return jsonify({"message": f"Content from {url} stored in index {index_name}", "tables_extracted": len(tables)}), 200

@app.route('/search', methods=['GET'])
def search_content():
    query = request.args.get('q')
    index_name = request.args.get('index_name', 'web_crawl_index')

    if not query:
        return jsonify({"error": "Search query is required"}), 400

    # Search in Elasticsearch
    result = es.search(index=index_name, query={"match": {"content": query}})

    return jsonify(result['hits']['hits'])

if __name__ == '__main__':
    app.run(debug=True)
