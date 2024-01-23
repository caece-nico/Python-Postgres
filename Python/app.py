from flask import Flask, request

app = Flask(__name__)


stores = [
    {
        "name": "My Store",
        "items":[
            {
                "name":"Chair",
                "Price":15.129
            }
        ]
    }
]

@app.get("/store")
def get_store():
    return {"stores": stores}