import requests
import os
import json
from datetime import datetime, timedelta

# EODHD API key
api_key = os.getenv("EODHD_API_KEY", "68765fba17e027.15367113")
base_url = "https://eodhd.com/api"

# Step 1: Get top percentage gainers
def get_top_gainers():
    url = f"{base_url}/screener"
    filters = [
        ["exchange", "in", ["NASDAQ", "NYSE"]],
        ["price", ">=", 1],
        ["price", "<=", 20],
        ["change_p", ">=", 10]
    ]
    params = {
        "api_token": api_key,
        "market": "US",
        "filters": json.dumps(filters),  # JSON-encode filters
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
    except requests.exceptions.HTTPError as e:
        print(f"EODHD screener request failed: {e}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return []
    except Exception as e:
        print(f"Unexpected error in screener: {e}")
        return []

# Step 2: Filter by float shares and relative volume
def filter_stocks(gainers):
    filtered_stocks = []
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    for stock in gainers:
        symbol = stock["code"]
        # Get fundamental data (float shares)
        url = f"{base_url}/fundamentals/{symbol}.US"
        params = {"api_token": api_key}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            float_shares = data.get("SharesStats", {}).get("SharesFloat", float("inf"))
            if float_shares and float_shares < 10_000_000:
                # Get intraday volume for relative volume
                intraday_url = f"{base_url}/intraday/{symbol}.US"
                params = {
                    "api_token": api_key,
                    "interval": "1h",
                    "from": start_date,
                    "to": end_date
                }
                response = requests.get(intraday_url, params=params)
                response.raise_for_status()
                intraday_data = response.json().get("data", [])
                if intraday_data:
                    today_volume = sum(d["volume"] for d in intraday_data if d["datetime"].startswith(end_date))
                    avg_volume = sum(d["volume"] for d in intraday_data) / len([d for d in intraday_data])
                    relative_volume = today_volume / avg_volume if avg_volume > 0 else 0
                    if relative_volume >= 5:
                        filtered_stocks.append({
                            "symbol": symbol,
                            "name": stock["name"],
                            "price": stock["price"],
                            "percent_change": stock["change_p"],
                            "volume": today_volume,
                            "relative_volume": relative_volume,
                            "float_shares": float_shares
                        })
        except requests.exceptions.HTTPError as e:
            print(f"Error for {symbol}: {e}")
        except Exception as e:
            print(f"Unexpected error for {symbol}: {e}")
    return filtered_stocks

# Run screener
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