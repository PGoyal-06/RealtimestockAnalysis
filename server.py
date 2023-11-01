# from flask import Flask, jsonify
# from ably import AblyRest

# app = Flask(__name__)
# ably = AblyRest('WnIRrA.xFlb_Q:m93uJLI1BHRHAotTYtV0XY8keVa6isAZRT8GhXZMbXg')

# @app.route('/data/<path:ticker_symbols>')
# def get_data(ticker_symbols):
#     data = {}
#     for ticker_symbol in ticker_symbols.split(','):
#         channel = ably.channels.get(ticker_symbol)
#         history_items = channel.history().items
#         print(f"Data for {ticker_symbol}: {history_items}")  # Check the AblyRest API data
#         data[ticker_symbol] = history_items
#     return jsonify(data)

# @app.route('/')
# def home():
#     return "Welcome to my realtime stock dashboard!"

# if __name__ == "__main__":
#     app.run(debug=True)

from fastapi import FastAPI
from ably import AblyRest
import asyncio

app = FastAPI()
ably = AblyRest('WnIRrA.HAR2lw:wdRstrLRRq9Y4i8ype6_QfllGjPOY8oD-yruzK7CbVM')

@app.get('/data/{ticker_symbols}')
async def get_data(ticker_symbols: str):
    data = {}
    for ticker_symbol in ticker_symbols.split(','):
        channel = ably.channels.get(ticker_symbol)
        history_items = await channel.history().items
        print(f"Data for {ticker_symbol}: {history_items}")  # Check the AblyRest API data
        if not history_items:
            print(f"No data returned for {ticker_symbol}")
        data[ticker_symbol] = history_items
    print(f"Data to be returned: {data}")  # Check the data before it's returned
    return data
