from flask import Flask
import time

app = Flask(__name__)

@app.route("/product/<int:product_id>")
def get_product(product_id):
    # simulating delay
    time.sleep(1)
    return {"product_id":product_id}

if __name__== "__main__":
    app.run(debug=True)
