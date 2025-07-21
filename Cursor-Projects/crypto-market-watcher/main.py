import os
import requests
import pandas as pd
import time
import schedule
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')

bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None

# 1. Get top 20 coins by market cap
def get_top_coins(n=20, vs_currency='usd'):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': vs_currency, 'order': 'market_cap_desc', 'per_page': n, 'page': 1}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return [coin['id'] for coin in r.json()]

# 2. Download 365 days of OHLC data for a coin
def get_ohlc(symbol, vs_currency='usd', days=365):
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/ohlc'
    params = {'vs_currency': vs_currency, 'days': days}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# 3. Get 24h price change for a coin
def get_24h_change(symbol, vs_currency='usd'):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': vs_currency, 'ids': symbol}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]['price_change_percentage_24h'], data[0]['current_price']
    return None, None

# 4. Alert for 5%+ change
def alert_price_change(symbol, change, price):
    if bot and TELEGRAM_USER_ID:
        msg = f"{symbol.capitalize()} price changed {change:.2f}% in 24h. Current price: ${price}"
        bot.send_message(chat_id=TELEGRAM_USER_ID, text=msg)
    print(f"ALERT: {symbol} {change:.2f}% (${price})")

# 5. Main job
def job():
    coins = get_top_coins(20)
    for coin in coins:
        print(f"Fetching {coin}...")
        try:
            df = get_ohlc(coin, 'usd', 365)
            df.to_csv(f'{coin}_ohlc_365d.csv', index=False)
            print(f"Saved {coin}_ohlc_365d.csv")
            change, price = get_24h_change(coin)
            if change is not None and abs(change) >= 5:
                alert_price_change(coin, change, price)
            time.sleep(2)  # Respect API rate limits
        except Exception as e:
            print(f"Error fetching {coin}: {e}")

if __name__ == '__main__':
    job()  # Run once at start
    schedule.every().hour.do(job)
    print("Running hourly. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(10) 