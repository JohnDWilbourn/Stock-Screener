import requests
import os

# Use environment variable for API key
polygon_api_key = os.getenv("POLYGON_API_KEY", "IGueCTadMWgZNLZf3pYxx52XD0sl0XgL")
# Polygon.io API endpoint (ticker metadata)
url = "https://api.polygon.io/v3/reference/tickers?market=stocks&limit=10"

# Make the API request
try:
    response = requests.get(url, params={"apiKey": polygon_api_key})
    response.raise_for_status()
    
    data = response.json()
    if data.get("status") == "OK":
        print("Polygon.io API Key is valid! Sample ticker data:")
        print(data.get("results", [])[:5])
    else:
        print("Polygon.io API Key is valid, but no data returned:", data)
        
except requests.exceptions.HTTPError as e:
    print(f"Polygon.io API request failed: {e}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"An error occurred with Polygon.io API: {e}")