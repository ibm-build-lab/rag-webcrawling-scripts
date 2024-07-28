# Webcrawling scripts using Beautiful Soup
This repo contains scripts used to crawl websites and store documents to be indexed for RAG solutions.

The order to run the scripts: 

1) run `get-urls-from-sitemap.py` to get urls from sitemap
2) run `get internal-links.py` to get internal urls not in sitemap
3) run `get-link-data.py` to get the data from the links
4) run `get-multithreaded-link-data.py` to get multithreaded info
5) run `get-all-link-data-multithreaded-info-into-db.py` to put data into database