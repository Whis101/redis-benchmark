from flask import Flask
import time
import redis 
import json
import os
#create app instance
app = Flask(__name__)

# create reuseable redis client instance
REDIS_HOST = os.getenv('REDIS_HOST','localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT',"6379"))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def fetch_prod_from_db(product_id):
    time.sleep(1)
    return {"product_id": product_id}

# define what happens when the user visits product id endpoint
@app.route("/product/<int:product_id>")
def get_product(product_id):
    cache_key = f"product:{product_id}"
    cached_val = redis_client.get(cache_key)
    if cached_val is not None:
        return json.loads(cached_val)
    result = fetch_prod_from_db(product_id)
    redis_client.set(cache_key, json.dumps(result),ex=30)
    return result

# running applciation
if __name__== "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
