from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS   # <- Import CORS
import random

app = Flask(__name__, static_url_path='', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins=["http://127.0.0.1:5000"])


stocks = [
    {"name": "Water Inc.", "ticker": "WTR", "price": 100.50, "historicalPrices": [99, 100, 101, 102], "highestPrice": 102, "lowestPrice": 99, "tradingVolume": 1000},
    {"name": "Air Corp.", "ticker": "AIR", "price": 110.25, "historicalPrices": [108, 109, 110, 111], "highestPrice": 111, "lowestPrice": 108, "tradingVolume": 1200},
    {"name": "Earth Ltd.", "ticker": "ERTH", "price": 90.75, "historicalPrices": [89, 90, 91, 92], "highestPrice": 92, "lowestPrice": 89, "tradingVolume": 980},
    {"name": "Fire Enterprises", "ticker": "FRE", "price": 120.80, "historicalPrices": [118, 119, 120, 121], "highestPrice": 121, "lowestPrice": 118, "tradingVolume": 1500},
]

@app.route('/')
def serve_client():
    return app.send_static_file('index.html')

@app.route('/stocks', methods=['GET'])
def get_stocks():
    return jsonify(stocks)

@app.route('/stocks', methods=['POST'])
def add_stock():
    new_stock = request.json
    stocks.append(new_stock)
    return jsonify(new_stock), 201

@socketio.on('request_stock_updates')
def send_stock_updates():
    # Simulate stock price changes
    for stock in stocks:
        stock["price"] += random.uniform(-1, 1)
    socketio.emit('stock_price_updates', stocks)

if __name__ == "__main__":
    socketio.run(app, debug=True)


