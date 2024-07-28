from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.common.exceptions import TimeoutException,NoSuchElementException

def init_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def click_affected_products_button(driver):
    try:
        button_xpath = "//button[span[contains(text(), 'AFFECTED PRODUCT SERIES / FEATURES')]]"
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'afftedProd')]"))
        )
    except TimeoutException:
        print("The button to show affected products was not found or not clickable.")
    except Exception as e:
        print(f"An error occurred while clicking on the button: {e}")
        
def navigate_to_url(driver, url):
    try:
        driver.get(url)
        driver.implicitly_wait(20)
        click_affected_products_button(driver)
    except Exception as e:
        print(f"An error occurred while navigating to the URL {url}: {e}")
        return None
    return driver.page_source


def extract_section_content(article_content, label_text):
    try:
        label = article_content.find('label', string=label_text)
        if label and label.next_sibling:
            return label.next_sibling.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"An error occurred while extracting {label_text}: {e}")
    return ""

def extract_affected_products(article_content):
    affected_products = []
    try:
        affected_products_section = article_content.find('div', {'class': 'afftedProd'})
        if affected_products_section:
            affected_product_tags = affected_products_section.find_all('a')
            for affected_product in affected_product_tags:
                affected_products.append({affected_product.get_text(): affected_product['href']})
    except Exception as e:
        print(f"An error occurred while extracting affected products: {e}")
    return affected_products

def process_url(url):
    driver = init_driver()
    try:
        page_source = navigate_to_url(driver, url)
        data = {}
        data["url"] = url
        if page_source:
            
            soup = bs(page_source, 'html.parser')

            # Extract metadata
            try:
                article_metadata = soup.find('div', {'class': 'titleSection'}).get_text(separator='\n')
                data["article_metadata"] = article_metadata
            except NoSuchElementException:
                print("Article metadata not found.")
                data["article_metadata"] = "Not found"

            # Extract detail sections
            article_content = soup.find('div', {'class': 'detailSection'})
            if article_content:
                data['Description'] = extract_section_content(article_content, 'Description')
                data['Symptoms'] = extract_section_content(article_content, 'Symptoms')
                data['Solution'] = extract_section_content(article_content, 'Solution')
                data['Fix'] = extract_section_content(article_content, 'Solution')
                data['Resolved-In'] = extract_section_content(article_content, 'Solution')
                data["Affected Products"] = extract_affected_products(article_content)
            else:
                print("Article content not found.")

        with open('results.jsonl', 'a+') as file:
            file.write(json.dumps(data) + '\n')
            
    except Exception as e:
        print(e)
    finally:
        driver.quit()

def main(urls):
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
                print(f"Completed {url}")
            except Exception as e:
                print(f"Error processing {url}: {e}")


if __name__ == "__main__":
    with open("./knowledge_base_links.json",'r') as file:
        urls = json.load(file)
        main(urls)
