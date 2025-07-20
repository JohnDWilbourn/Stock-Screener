import requests
import os
import json

# EODHD API key
api_key = os.getenv("EODHD_API_KEY", "68765fba17e027.15367113")
url = "https://eodhd.com/api/screener"

# Test top gainers
params = {
    "api_token": api_key,
    "market": "US",
    "limit": 10,
    "filters": json.dumps([
        ["exchange", "in", ["NASDAQ", "NYSE"]],
        ["last_price", ">=", 1],
        ["last_price", "<=", 20],
        ["change_pct", ">=", 10]
    ]),
    "sort": "change_pct.desc"
}
try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if data.get("status") == "ok":
        print("EODHD API Key is valid! Top 10 US gainers:")
        for stock in data.get("data", [])[:10]:
            print(f"{stock['code']}: {stock['name']}, Price: ${stock['last_price']:.2f}, Change: {stock['change_pct']:.2f}%")
    else:
        print("No data returned:", data)
except requests.exceptions.HTTPError as e:
    print(f"EODHD screener request failed: {e}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")