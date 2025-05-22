from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STEALTHEX_API_KEY = '6915ba2c-6817-4bf0-b1cb-e1e7e2c21733'  # Replace this with your real key

@app.route('/render-swap', methods=['POST'])
def render_swap():
    data = request.json
    from_coin = data['from']
    to_coin = data['to']
    amount = float(data['amount'])
    wallet = data['wallet']

    # Apply 5% fee
    fee_amount = round(amount * 1.05, 8)

    # Step 1: Get exchange info
    response = requests.get(f'https://api.stealthex.io/api/v2/estimate-fixed-rate', params={
        'fixed': 'true',
        'currencyFrom': from_coin,
        'currencyTo': to_coin,
        'amountFrom': fee_amount,
        'api_key': STEALTHEX_API_KEY
    })

    quote = response.json()
    if not quote or 'estimatedAmount' not in quote[0]:
        return jsonify({'error': 'Could not get estimate'}), 400

    # Step 2: Create exchange
    exchange = requests.post('https://api.stealthex.io/api/v2/exchange', json={
        'fixed': True,
        'currencyFrom': from_coin,
        'currencyTo': to_coin,
        'amountFrom': fee_amount,
        'addressTo': wallet,
        'api_key': STEALTHEX_API_KEY
    })

    return jsonify(exchange.json())
