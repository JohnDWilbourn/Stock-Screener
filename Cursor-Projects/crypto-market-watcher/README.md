# Crypto Market Watcher

Automated CoinGecko downloader with Telegram alerts for 5% price changes in the top 20 coins.

## Features
- Downloads 365 days of OHLC data for the top 20 coins
- Sends Telegram alerts for 5%+ price changes (real-time)
- Runs hourly (can be customized)

## Setup
1. Clone this repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Telegram bot token and user ID:
   ```
   TELEGRAM_TOKEN=your_bot_token
   TELEGRAM_USER_ID=your_user_id
   ```
4. Run the script:
   ```
   python main.py
   ``` 