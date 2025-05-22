from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Crypto Swap API is running!"

@app.route('/render-swap', methods=['POST'])
def render_swap():
    data = request.get_json()
    
    # Get swap details
    from_coin = data.get("from_coin")
    to_coin = data.get("to_coin")
    amount = data.get("amount")
    wallet_address = data.get("wallet_address")

    # Simple response for now
    return jsonify({
        "status": "success",
        "message": f"Swapped {amount} {from_coin} to {to_coin} for wallet {wallet_address}"
    })
