import requests
from dotenv import load_dotenv
import os
import datetime
import hashlib
import hmac

# Load environment variables from .env file
load_dotenv()
amazon_api_key = os.getenv("AMAZON_API_KEY")
amazon_secret_key = os.getenv("AMAZON_SECRET_KEY")
amazon_associate_tag = os.getenv("AMAZON_ASSOCIATE_TAG")

def fetch_books_from_amazon(mood):
    endpoint = "webservices.amazon.com"
    uri = "/onca/xml"
    
    params = {
        "Service": "AWSECommerceService",
        "Operation": "ItemSearch",
        "AWSAccessKeyId": amazon_api_key,
        "AssociateTag": amazon_associate_tag,
        "SearchIndex": "Books",
        "Keywords": mood,
        "ResponseGroup": "Images,ItemAttributes,Offers"
    }
    
    # Timestamp and signature
    params["Timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    sorted_params = sorted(params.items())
    canonical_query_string = "&".join(["{}={}".format(k, v) for k, v in sorted_params])
    string_to_sign = "GET\n{}\n{}\n{}".format(endpoint, uri, canonical_query_string)
    
    signature = hmac.new(amazon_secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    signature = requests.utils.quote(signature, safe='')
    
    request_url = "https://{}{}?{}&Signature={}".format(endpoint, uri, canonical_query_string, signature)
    
    response = requests.get(request_url)
    books_data = response.json()  # Assuming the response is JSON; adjust if necessary
    return books_data
