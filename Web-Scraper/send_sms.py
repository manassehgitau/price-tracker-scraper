import africastalking
import math
from decouple import config
from pymongo import MongoClient
from scrapers.query_product import make_comparison

username = config('AFRICAS_TALKING_USERNAME')
api_key = config('AFRICAS_TALKING_API_KEY')
africastalking.initialize(username, api_key)

sms =  africastalking.SMS

mongo_uri = config('MONGODB_URI')
client = MongoClient(mongo_uri)
database = client['priceTracker']
users_collection = database['users']

def clean_price(price_str):
    if not price_str:
        return 0.0
    cleaned = price_str.replace("KSh", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def send_sms(product_name, phone_number):
    products_matched = make_comparison(product_name)

    if len(products_matched) > 0:
        for product in products_matched:

            # TODO: Clean the data from carrefour and jumia when scraping and must have a similar structure

            message = f'''
found a match with a score of \n{math.floor(product["score"])} with the details below \n
Store: {product["store"]}, \n
Name: {product["Name"]}, \n
Price: {product["Price"]}, \n
Category: {product["category"]}, \n
Find the Image using {product["Image URL"]}
            '''

            sms.send(message, [phone_number])    
    else:
        message = "No products are found matching that criteria"
        sms.send(message, [phone_number])    
        