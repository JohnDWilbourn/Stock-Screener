from polygon import RESTClient

# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
client = RESTClient(api_key="YOUR_API_KEY")

snapshot = client.get_snapshot_all("stocks")
for stock in snapshot:
    if stock.last_trade.price >= 1 and stock.last_trade.price <= 20:
        print(stock.ticker, stock.last_trade.price, stock.day.volume)