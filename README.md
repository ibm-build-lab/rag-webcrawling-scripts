# Webcrawling scripts using Beautiful Soup
This repo contains scripts used to crawl websites and store documents to be indexed for RAG solutions.

How to run these scripts locally: 

1. Clone this repository

2. Navigate to the project directory:

    ```bash
    cd <your-project>
    ```

3. Create the Enviroment, Activate it

    Python Virtual Environment

    ```bash
    python -m venv assetEnv
    source assetEnv/bin/activate
    ```
5. Run the scripts:

    ```bash
    python <script>.py
    ```
The order to run the scripts: 

1) run `get-urls-from-sitemap.py` to get urls from sitemap
2) run `get-internal-links.py` to get internal urls not in sitemap
3) run `get-all-link-data.py` to get the data from the links

Use multithreading for faster crawling and answer saving. Some of the requests may be blocked by the host website or it is unable to handle the load at that time. This approach is to get the missing urls and rerun the script with multithreading, little bit manual but still much faster.

4) run `get-multithreaded-link-data.py` to get data using multi threaded approach
5) run `get-all-link-data-multithreaded-info-into-db.py` to put data into database
6) run `get-documentation-page-data.py` parse html page data, including tables

Helper scripts:

- `pdf-links.py`: get all pdfs from urls links
- `get-article.py`: navigate to article within html page
- `convert-jsonl-to-json.py`: converts newline JSON to JSON
- `find-missing-links.py`: Verify that links from .csv are in fact missing

## Additional scripts to do webcrawling: 

[app_webcrawl.py](./app_webcrawl.py)
[app_webcrawl_complex.py](./app_webcrawl_complex.py)