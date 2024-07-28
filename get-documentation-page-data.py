import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from io import StringIO
import traceback
# Define a dictionary with multiple patterns
patterns = {
    "Pattern1": {
        "content": {"tag": "div", "class": "l-body"}
    },
    "Pattern2": {
        "content": {"tag": "div", "id": "topic-content"}
    },
    "Pattern3": {
        "content": {"tag": "div", "class": "content"}
    },
    
    "Pattern4": {
        "content": {"tag": "div", "class": "product-page"}
    } 
}

def fetch_data(url,wait_per_page=5):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(wait_per_page) 
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "html.parser")
    published_date = ""
    meta_description = ""
    for pattern_name, pattern in patterns.items():
        try:
            content_selector = pattern["content"]
            
            # Construct title and content find parameters
            content_params = {content_selector.get("class_type", "class"): content_selector.get("class")} if content_selector.get("class") else {}
            
            if "id" in content_selector:
                content_params["id"] = content_selector["id"]
            
            page_title = soup.find('title').get_text(separator="\n",strip=True)
            main_content_element = soup.find(content_selector["tag"], content_params)
            # Extract tables and convert to JSON
            tables = main_content_element.find_all('table')
            tables_json = [pd.read_html(str(table))[0].to_json(orient='records') for table in tables]
            
            try:
                meta_description = soup.find('meta', {'name': 'description'})['content']
            except:
                pass
            # getting published_date
            try:
                published_date = soup.find("div","pbdate").get_text(separator="\n",strip=True).replace('date_range','')
            except:
                pass 
                
            
            # Remove tables from the main content
            for table in tables:
                table.decompose()
            main_content_text = main_content_element.get_text(separator="\n",strip=True)
            content_length = len(main_content_text)

            # If successful, return the data with the pattern name
            return {"link": url, "title": page_title,"published_date":published_date,"meta-description":meta_description, "main_content": main_content_text, "content_length": content_length,"tables":tables_json, "pattern_used": pattern_name}
        except Exception as e:
            # If a pattern fails, print an error message and continue with the next pattern
            print(f"Error with {pattern_name}: {e}")
            continue

    # If no pattern worked, return
    try:
        main_content_element = soup.find("body")
        # Extract tables and convert to JSON
        page_title = soup.find('title').get_text(separator="\n",strip=True)
        tables = main_content_element.find_all('table')
        tables_json = [pd.read_html(str(table))[0].to_json(orient='records') for table in tables]
        try:
            meta_description = soup.find('meta', {'name': 'description'})['content']
        except:
            pass
        # Remove tables from the main content
        for table in tables:
            table.decompose()
        main_content_text = main_content_element.get_text(separator="\n",strip=True)
        content_length = len(main_content_text)
        pattern_used = "Default"
        published_date = ""
        # getting published_date
        try:
            published_date = soup.find("div","pbdate").get_text(separator="\n",strip=True).replace('date_range','')
        except:
            pass 
                     
    except Exception as e:
        main_content_text = ""
        pattern_used = "Default-NULL"
        tables_json={}
        
    data = {"link": url, "title": page_title,"published_date":published_date,"meta-description":meta_description, "main_content":main_content_text , "content_length": len(main_content_text),"tables":tables_json, "pattern_used": pattern_used}
    
    return data

if __name__ == "__main__":
    url = "https://www.company.net/documentation/us/en/software/release-notes/22.1/release-notes.html"
    data = fetch_data(url)
    print(data if data else "data not found.")
