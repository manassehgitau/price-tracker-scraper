from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import requests
import time
from urls import carrefour_urls
from pymongo import MongoClient
from decouple import config

mongo_uri = config('MONGODB_URI')
client = MongoClient(mongo_uri)
database = client['priceTracker']
collection = database["Carrefour_Products"]

# Delete all documents that exist in DB
query_filter = {"store": "Carrefour"}
result = collection.delete_many(query_filter, comment="Deletion completed")
print("Deleted Items: ", result.deleted_count)

for category, section_url in carrefour_urls.items():
    url  = section_url
    path = '/usr/local/bin/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    print(url)


    while True:
        try:
            # Wait for and click the "Load More" button if it exists
            load_more_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "css-10s9ah"))
            )
            load_more_button.click()
            time.sleep(10)  

            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                break

        except TimeoutException:
            print("No more 'Load More' button or it's not clickable.")
            break
        except ElementClickInterceptedException:
            print("Click intercepted, possibly due to a popup or overlay.")
            break

    products = driver.find_elements(By.CLASS_NAME, "css-1omnv59")

    for product in products:
        try:
            product_image = product.find_element(By.CLASS_NAME, "css-1npvvk7").find_element(By.TAG_NAME, "img").get_attribute("src")
            product_name = product.find_element(By.CLASS_NAME, "css-tuzc44").find_element(By.TAG_NAME, "a").get_attribute("title")
            product_price_num = product.find_element(By.CLASS_NAME, "css-14zpref").text
            product_price_decimal = product.find_element(By.CLASS_NAME, "css-1pjcwg4").text
            product_price = product_price_num + product_price_decimal
            product_price_currency = product.find_element(By.CLASS_NAME, "css-1edki26").text

            try:
                offer_tag = product.find_element(By.CSS_SELECTOR, '[data-testid="headerStickerId"]')
                is_on_offer = True
                percentage_discount = offer_tag.text
            except NoSuchElementException:
                is_on_offer = False
                percentage_discount = "0"

            product_db_list = {
                    "category": category,
                    "store":  "Carrefour",
                    "Name" : product_name,
                    "Price" : f"{product_price_currency} {product_price}",
                    "Image URL" : product_image,
                    "On Offer" : is_on_offer,
                    "Discount" : percentage_discount,
                  }
                
            result = collection.insert_one(product_db_list)
            time.sleep(1)
            print(result.acknowledged)

        except Exception as e:
            print(f"Error reading product: {e}")
            continue

time.sleep(5)
driver.quit()
