from rapidfuzz import fuzz
from pymongo import MongoClient
from decouple import config
import re

mongo_uri = config('MONGODB_URI')
client = MongoClient(mongo_uri)
database = client['priceTracker']

jumia_collection = database["Jumia_Products"]
carrefour_collection = database["Carrefour_Products"]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  
    text = re.sub(r'\s+', ' ', text).strip()  
    return text


def make_comparison(product_name):
    all_products =  list(jumia_collection.find()) + list(carrefour_collection.find())

    product_name_clean = clean_text(product_name)

    matched = []
    for product in all_products:
        db_product_name = product.get("Name", "")
        db_product_name_clean = clean_text(db_product_name)

        ratio = fuzz.token_set_ratio(product_name_clean, db_product_name_clean)
        if ratio >= 70:
            matched.append({**product, "score": ratio})

    if matched:
        matched = sorted(matched, key=lambda x: x.get("score", float('inf')))

    return matched
# make_comparison("paprika")
