import requests

# EODHD API key
eodhd_api_key = "68765fba17e027.15367113"
# EODHD API endpoint (example: get stock price for AAPL)
url = "https://eodhd.com/api/eod/AAPL.US"

# Make the API request
try:
    response = requests.get(url, params={"api_token": eodhd_api_key, "fmt": "json"})
    response.raise_for_status()  # Check for HTTP errors
    
    # Check if the response contains data
    data = response.json()
    if data:
        print("EODHD API Key is valid! Sample data for AAPL:")
        print(data[:5])  # Print first 5 entries for brevity
    else:
        print("EODHD API Key is valid, but no data returned.")
        
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        print("EODHD API Key is invalid or unauthorized.")
    else:
        print(f"EODHD API request failed: {e}")
except Exception as e:
    print(f"An error occurred with EODHD API: {e}")