import os
from dotenv import load_dotenv
from polygon import RESTClient

"""
Polygon.io Stock Screener
- Loads API key securely from .env
- Fetches all stock snapshots
- Prints tickers with last trade price between $1 and $20
"""

load_dotenv()
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')

if not POLYGON_API_KEY:
    raise ValueError("Polygon.io API key not found. Please set POLYGON_API_KEY in your .env file.")

client = RESTClient(api_key=POLYGON_API_KEY)

try:
    snapshot = client.get_snapshot_all("stocks")
    for stock in snapshot:
        price = getattr(stock.last_trade, 'price', None)
        if price is not None and 1 <= price <= 20:
            print(f"{stock.ticker}: ${price:.2f} | Volume: {stock.day.volume}")
except Exception as e:
    print(f"Error fetching Polygon.io data: {e}")