import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
POLYGON_BASE_URL = 'https://api.polygon.io'

class StockScreener:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = POLYGON_BASE_URL
        
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def get_all_tickers(self, market='stocks', active=True, limit=1000):
        """Get all available stock tickers"""
        url = f"{self.base_url}/v3/reference/tickers"
        params = {
            'market': market,
            'active': active,
            'limit': limit,
            'apikey': self.api_key
        }
        
        all_tickers = []
        next_url = None
        
        try:
            while True:
                if next_url:
                    response = requests.get(next_url)
                else:
                    response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data:
                        all_tickers.extend(data['results'])
                    
                    # Check for pagination
                    if 'next_url' in data:
                        next_url = data['next_url'] + f"&apikey={self.api_key}"
                    else:
                        break
                else:
                    print(f"Error fetching tickers: {response.status_code}")
                    break
                
                # Respect rate limits
                time.sleep(0.1)
                
                # Limit to prevent too many requests
                if len(all_tickers) >= 5000:
                    break
            
            return all_tickers
        except Exception as e:
            print(f"Error in get_all_tickers: {e}")
            return []
    
    def get_stock_snapshot(self, ticker):
        """Get current snapshot data for a stock"""
        url = f"{self.base_url}/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and 'value' in data['results']:
                    return data['results']['value']
            return None
        except Exception as e:
            print(f"Error getting snapshot for {ticker}: {e}")
            return None
    
    def get_previous_close(self, ticker):
        """Get previous close data for a stock"""
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    return data['results'][0]
            return None
        except Exception as e:
            print(f"Error getting previous close for {ticker}: {e}")
            return None
    
    def get_sma(self, ticker, window=50, timespan='day', limit=60):
        """Get Simple Moving Average for a stock"""
        url = f"{self.base_url}/v1/indicators/sma/{ticker}"
        params = {
            'timespan': timespan,
            'adjusted': 'true',
            'window': window,
            'series_type': 'close',
            'order': 'desc',
            'limit': limit,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and 'values' in data['results'] and len(data['results']['values']) > 0:
                    return data['results']['values'][0]['value']
            return None
        except Exception as e:
            print(f"Error getting SMA for {ticker}: {e}")
            return None
    
    def get_rsi(self, ticker, window=14, timespan='day', limit=30):
        """Get RSI for a stock"""
        url = f"{self.base_url}/v1/indicators/rsi/{ticker}"
        params = {
            'timespan': timespan,
            'adjusted': 'true',
            'window': window,
            'series_type': 'close',
            'order': 'desc',
            'limit': limit,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and 'values' in data['results'] and len(data['results']['values']) > 0:
                    return data['results']['values'][0]['value']
            return None
        except Exception as e:
            print(f"Error getting RSI for {ticker}: {e}")
            return None
    
    def get_ticker_details(self, ticker):
        """Get detailed information about a ticker"""
        url = f"{self.base_url}/v3/reference/tickers/{ticker}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    return data['results']
            return None
        except Exception as e:
            print(f"Error getting ticker details for {ticker}: {e}")
            return None

# Initialize screener
screener = StockScreener(POLYGON_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tickers')
def get_tickers():
    """Get list of available tickers"""
    try:
        tickers = screener.get_all_tickers(limit=500)  # Limit for performance
        # Filter for major stocks and ETFs
        filtered_tickers = []
        for ticker in tickers:
            if (ticker.get('market') == 'stocks' and 
                ticker.get('active') == True and
                ticker.get('type') in ['CS', 'ETF'] and  # Common Stock or ETF
                len(ticker.get('ticker', '')) <= 5):  # Filter out complex tickers
                filtered_tickers.append({
                    'ticker': ticker.get('ticker'),
                    'name': ticker.get('name'),
                    'type': ticker.get('type'),
                    'market_cap': ticker.get('market_cap')
                })
        
        return jsonify({'tickers': filtered_tickers[:1000]})  # Limit response size
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screen', methods=['POST'])
def screen_stocks():
    """Screen stocks based on criteria"""
    try:
        criteria = request.json
        
        # Get sample of popular tickers for screening
        popular_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B', 'LLY', 'V',
            'JPM', 'UNH', 'XOM', 'MA', 'PG', 'JNJ', 'HD', 'CVX', 'ABBV', 'MRK',
            'COST', 'BAC', 'PEP', 'TMO', 'AVGO', 'WMT', 'LIN', 'NFLX', 'DIS', 'ABT',
            'CRM', 'ACN', 'CSCO', 'AMD', 'DHR', 'VZ', 'ADBE', 'TXN', 'NEE', 'PM',
            'RTX', 'NKE', 'T', 'LOW', 'SPGI', 'QCOM', 'UNP', 'HON', 'AMAT', 'AXP'
        ]
        
        results = []
        
        for ticker in popular_tickers:
            try:
                # Get basic data
                prev_close = screener.get_previous_close(ticker)
                if not prev_close:
                    continue
                
                current_price = prev_close['c']
                volume = prev_close['v']
                change = prev_close['c'] - prev_close['o']
                change_percent = (change / prev_close['o']) * 100
                
                # Get technical indicators
                sma_50 = screener.get_sma(ticker, 50)
                rsi = screener.get_rsi(ticker)
                
                # Get ticker details for market cap
                details = screener.get_ticker_details(ticker)
                market_cap = details.get('market_cap') if details else None
                
                stock_data = {
                    'ticker': ticker,
                    'name': details.get('name', ticker) if details else ticker,
                    'price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'volume': volume,
                    'market_cap': market_cap,
                    'sma_50': sma_50,
                    'rsi': rsi,
                    'price_to_sma_ratio': (current_price / sma_50) if sma_50 else None
                }
                
                # Apply filters
                if passes_filters(stock_data, criteria):
                    results.append(stock_data)
                
                # Rate limiting
                time.sleep(0.12)  # ~8 requests per second to stay within limits
                
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue
        
        # Sort results
        sort_by = criteria.get('sort_by', 'change_percent')
        reverse = criteria.get('sort_order', 'desc') == 'desc'
        
        results.sort(key=lambda x: x.get(sort_by, 0) or 0, reverse=reverse)
        
        return jsonify({'results': results[:50]})  # Limit to top 50 results
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def passes_filters(stock_data, criteria):
    """Check if stock passes the screening criteria"""
    try:
        # Price filter
        if criteria.get('min_price') and stock_data['price'] < criteria['min_price']:
            return False
        if criteria.get('max_price') and stock_data['price'] > criteria['max_price']:
            return False
        
        # Volume filter
        if criteria.get('min_volume') and stock_data['volume'] < criteria['min_volume']:
            return False
        
        # Market cap filter
        if criteria.get('min_market_cap') and stock_data.get('market_cap'):
            if stock_data['market_cap'] < criteria['min_market_cap']:
                return False
        
        # Change percent filter
        if criteria.get('min_change_percent') and stock_data['change_percent'] < criteria['min_change_percent']:
            return False
        if criteria.get('max_change_percent') and stock_data['change_percent'] > criteria['max_change_percent']:
            return False
        
        # RSI filter
        if criteria.get('min_rsi') and stock_data.get('rsi'):
            if stock_data['rsi'] < criteria['min_rsi']:
                return False
        if criteria.get('max_rsi') and stock_data.get('rsi'):
            if stock_data['rsi'] > criteria['max_rsi']:
                return False
        
        # Price vs SMA filter
        if criteria.get('price_above_sma') and stock_data.get('price_to_sma_ratio'):
            if stock_data['price_to_sma_ratio'] < 1.0:
                return False
        
        return True
    except Exception as e:
        print(f"Error in filter check: {e}")
        return False

@app.route('/api/stock/<ticker>')
def get_stock_details(ticker):
    """Get detailed information for a specific stock"""
    try:
        details = screener.get_ticker_details(ticker)
        prev_close = screener.get_previous_close(ticker)
        sma_50 = screener.get_sma(ticker, 50)
        sma_200 = screener.get_sma(ticker, 200)
        rsi = screener.get_rsi(ticker)
        
        if not details or not prev_close:
            return jsonify({'error': 'Stock not found'}), 404
        
        result = {
            'ticker': ticker,
            'name': details.get('name'),
            'description': details.get('description'),
            'market_cap': details.get('market_cap'),
            'employees': details.get('total_employees'),
            'website': details.get('homepage_url'),
            'sector': details.get('sic_description'),
            'current_price': prev_close['c'],
            'previous_close': prev_close['c'],
            'volume': prev_close['v'],
            'high': prev_close['h'],
            'low': prev_close['l'],
            'open': prev_close['o'],
            'change': prev_close['c'] - prev_close['o'],
            'change_percent': ((prev_close['c'] - prev_close['o']) / prev_close['o']) * 100,
            'sma_50': sma_50,
            'sma_200': sma_200,
            'rsi': rsi
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)