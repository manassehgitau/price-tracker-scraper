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

    # Fetch the user document first
    user = users_collection.find_one({"phone_number": phone_number})

    if not user:
        sms.send("User not found. Please sign up first.", [phone_number])
        return

    sms_tokens = user.get('sms tokens', 0)

    if sms_tokens <= 0:
        sms.send("Not enough tokens. Please purchase more tokens to use the service.", [phone_number])
        return

    if len(products_matched) > 0:
        for product in products_matched:
            message = f'''
Found a match with a score of {math.floor(product["score"])}:
Store: {product["store"]}
Name: {product["Name"]}
Price: {product["Price"]}
Category: {product["category"]}
Image: {product["Image URL"]}
            '''

            sms.send(message.strip(), [phone_number])

            # Deduct a token and update the DB
            sms_tokens -= 1
            users_collection.update_one(
                {"phone_number": phone_number},
                {"$set": {"sms tokens": sms_tokens}}
            )
    else:
        sms.send("No products found matching your search. Please try another product.", [phone_number])
