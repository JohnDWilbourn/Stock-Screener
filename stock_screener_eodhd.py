import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

"""
EODHD Stock Screener
- Loads API key securely from .env
- Gets top percentage gainers
- Filters by float shares and relative volume
- Prints results in a readable format
"""

load_dotenv()
EODHD_API_KEY = os.getenv('EODHD_API_KEY')

if not EODHD_API_KEY:
    raise ValueError("EODHD API key not found. Please set EODHD_API_KEY in your .env file.")

base_url = "https://eodhd.com/api"

def get_top_gainers():
    """Fetch top US gainers with price $1-$20 and >10% change."""
    url = f"{base_url}/screener"
    filters = [
        ["exchange", "in", ["NASDAQ", "NYSE"]],
        ["price", ">=", 1],
        ["price", "<=", 20],
        ["change_p", ">=", 10]
    ]
    params = {
        "api_token": EODHD_API_KEY,
        "market": "US",
        "filters": json.dumps(filters),
        "sort": "change_p.desc",
        "limit": 50
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            return data.get("data", [])
        else:
            print("No gainers data:", data)
            return []
    except Exception as e:
        print(f"Error in get_top_gainers: {e}")
        return []

def filter_stocks(gainers):
    """Filter gainers by float shares <10M and relative volume."""
    filtered_stocks = []
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    for stock in gainers:
        symbol = stock["code"]
        # Get fundamental data (float shares)
        url = f"{base_url}/fundamentals/{symbol}.US"
        params = {"api_token": EODHD_API_KEY}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            float_shares = data.get("SharesStats", {}).get("SharesFloat", float("inf"))
            if float_shares and float_shares < 10_000_000:
                # Get intraday volume for relative volume
                intraday_url = f"{base_url}/intraday/{symbol}.US"
                params = {
                    "api_token": EODHD_API_KEY,
                    "interval": "1h",
                    "from": start_date,
                    "to": end_date
                }
                response = requests.get(intraday_url, params=params)
                response.raise_for_status()
                intraday_data = response.json().get("data", [])
                if intraday_data:
                    volumes = [bar.get("volume", 0) for bar in intraday_data if bar.get("volume")]
                    avg_volume = sum(volumes) / len(volumes) if volumes else 0
                    rel_volume = stock.get("volume", 0) / avg_volume if avg_volume else 0
                    if rel_volume >= 5:
                        filtered_stocks.append({
                            "symbol": symbol,
                            "name": stock.get("name", ""),
                            "price": stock.get("price", 0),
                            "percent_change": stock.get("change_p", 0),
                            "volume": stock.get("volume", 0),
                            "relative_volume": rel_volume,
                            "float_shares": float_shares
                        })
        except Exception as e:
            print(f"Error filtering {symbol}: {e}")
    return filtered_stocks

if __name__ == "__main__":
    gainers = get_top_gainers()
    if gainers:
        results = filter_stocks(gainers)
        print("Top Gainers (Price $1-$20, >10% Up, <10M Float, 5x Volume):")
        for stock in results:
            print(f"{stock['symbol']}: {stock['name']}, Price: ${stock['price']:.2f}, "
                  f"Change: {stock['percent_change']:.2f}%, Volume: {stock['volume']}, "
                  f"Rel Volume: {stock['relative_volume']:.2f}x, Float: {stock['float_shares']}")
    else:
        print("No stocks found matching criteria.")