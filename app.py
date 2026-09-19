from flask import Flask
import time
import redis 
import json
#create app instance
app = Flask(__name__)

# create reuseable redis client instance
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# define what happens when the user visits product id endpoint
@app.route("/product/<int:product_id>")
def get_product(product_id):
    cache_key = f"product:{product_id}"
    cached_val = redis_client.get(cache_key)
    if cached_val is not None:
        return json.loads(cached_val)
    time.sleep(1)
    result = {"product_id": product_id}
    redis_client.set(cache_key, json.dumps(result),ex=30)
    return result

# running applciation
if __name__== "__main__":
    app.run(debug=True)
