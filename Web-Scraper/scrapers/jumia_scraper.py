from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapers.urls import jumia_urls 
from pymongo import MongoClient
from decouple import config

mongo_uri = config('MONGODB_URI')
client = MongoClient(mongo_uri)
database = client['priceTracker']
collection = database["Jumia_Products"]

query_filter = {"store": "Jumia"}
result = collection.delete_many(query_filter, comment="Deletion completed")
print("Deleted Items: ", result.deleted_count)

# Setup Chrome WebDriver
path = '/usr/local/bin/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

for category, section_url in jumia_urls.items():
    page = 1
    while True:
        url = section_url.format(page)
        print(url)

        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.prd"))
            )
        except:
            print("Timeout or no products found.")
            break

        # Now get all product elements
        products = driver.find_elements(By.CSS_SELECTOR, "article.prd")

        if not products:
            print("No Products Found")
            break

        for product in products:
            try:
                product_name = product.find_element(By.CLASS_NAME, "name").text
                current_price = product.find_element(By.CLASS_NAME, "prc").text
                
                try:
                    previous_price = product.find_element(By.CLASS_NAME, "old").text
                except:
                    previous_price = "NaN"

                image_url = product.find_element(By.CSS_SELECTOR, "img.img").get_attribute("src")
                
                try:
                    product.find_element(By.CSS_SELECTOR, "div.bdg._mall._xs")
                    from_official_store = True
                except:
                    from_official_store = False

                product_db_list = {
                    "category": category,
                    "store":  "Jumia",
                    "Name" : product_name,
                    "Price" : current_price,
                    "Previous Price" : previous_price,
                    "Image URL" : image_url,
                    "IsFromOfficialStore" : from_official_store,
                  }
                
                result = collection.insert_one(product_db_list)
                time.sleep(1)
                print(result.acknowledged)

            except Exception as e:
                print(f"Error reading product: {e}")
                continue

        page += 1

driver.quit()
client.close()