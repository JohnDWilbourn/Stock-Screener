# Stock Screener - Polygon.io API

A comprehensive stock screening application built with Flask and the Polygon.io API. This tool allows you to filter and analyze stocks based on various financial metrics and technical indicators.

## Features

### 📊 Stock Screening Capabilities
- **Price Filtering**: Set minimum and maximum price ranges
- **Volume Filtering**: Filter stocks by trading volume
- **Market Cap Filtering**: Screen by company size (Small, Mid, Large, Mega cap)
- **Performance Filtering**: Filter by daily change percentage
- **Technical Analysis**: RSI range filtering and SMA comparison
- **Sorting Options**: Sort results by various metrics (price, volume, change%, etc.)

### 📈 Technical Indicators
- **Simple Moving Average (SMA)**: 50-day and 200-day SMA
- **Relative Strength Index (RSI)**: 14-day RSI calculation
- **Price vs SMA**: Filter stocks trading above/below moving averages

### 💼 Company Information
- Market capitalization
- Employee count
- Sector information
- Company description
- Website links
- Stock exchange information

### 🎨 Modern UI Features
- Responsive design that works on desktop and mobile
- Glass morphism design with gradient backgrounds
- Interactive stock details modal
- Real-time loading indicators
- Color-coded price changes (green/red)
- Sortable results table

## Prerequisites

- Python 3.8 or higher
- Polygon.io API key ($29 Starter tier or higher)

## Installation

1. **Clone or download the project files**

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Polygon.io API key:
     ```
     POLYGON_API_KEY=your_polygon_api_key_here
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## Polygon.io API Features Used

With your $29 Starter tier, this application utilizes:

- **Ticker Details**: Company information and metadata
- **Previous Close**: Daily OHLCV data
- **Technical Indicators**: SMA and RSI calculations
- **Snapshots**: Current market data
- **Reference Data**: Ticker lists and company fundamentals

## Usage Guide

### Basic Screening
1. **Set Your Criteria**: Use the filter form to set your screening parameters
2. **Click "Screen Stocks"**: The app will analyze popular stocks against your criteria
3. **Review Results**: Results are displayed in a sortable table
4. **View Details**: Click on any stock row to see detailed information

### Filter Options

#### Price Range
- Set minimum and maximum price levels
- Useful for finding stocks in specific price ranges

#### Volume Filter
- Filter by minimum daily volume
- Example: Set to 1,000,000 to find actively traded stocks

#### Market Cap Categories
- **Small Cap**: $300M - $2B
- **Mid Cap**: $2B - $10B  
- **Large Cap**: $10B - $100B
- **Mega Cap**: $100B+

#### Change Percentage
- Filter by daily performance
- Find gainers (min 5%) or losers (max -5%)

#### RSI Range
- **Oversold**: RSI < 30
- **Overbought**: RSI > 70
- **Neutral**: RSI 30-70

#### Technical Filters
- **Price above 50 SMA**: Find stocks in uptrends
- Useful for momentum trading strategies

### Sorting Options
- **Change %**: Find biggest movers
- **Volume**: Most actively traded
- **Price**: Highest/lowest priced stocks
- **Market Cap**: Largest/smallest companies
- **RSI**: Most oversold/overbought

## API Rate Limits

The application includes built-in rate limiting to respect Polygon.io's API limits:
- Approximately 8-10 requests per second
- Automatic delays between requests
- Error handling for rate limit responses

## Sample Screening Strategies

### Growth Stocks
- Min Price: $10
- Min Volume: 1,000,000
- Min Change %: 5%
- Price above 50 SMA: Yes
- Sort by: Change %

### Value Opportunities  
- Max Price: $50
- Min Market Cap: Large Cap
- Max RSI: 40
- Sort by: Market Cap

### High Volume Breakouts
- Min Volume: 5,000,000
- Min Change %: 3%
- Price above 50 SMA: Yes
- Sort by: Volume

## Technical Details

### Backend (Flask)
- RESTful API endpoints
- Polygon.io API integration
- Data processing and filtering
- Rate limiting and error handling

### Frontend (HTML/CSS/JavaScript)
- Tailwind CSS for styling
- Vanilla JavaScript for interactivity
- Responsive design
- Glass morphism UI effects

### Data Sources
- **Real-time Data**: 15-minute delayed (Starter tier)
- **Historical Data**: Up to 5 years
- **Technical Indicators**: Server-side calculations via Polygon.io
- **Company Data**: SEC filings and reference data

## Troubleshooting

### Common Issues

1. **"API Key not found"**
   - Ensure your `.env` file exists and contains your API key
   - Verify the API key is correct

2. **"No results found"**
   - Try broader filter criteria
   - Some technical indicators may not be available for all stocks

3. **Slow responses**
   - The app processes multiple API calls for screening
   - Initial requests may take 30-60 seconds

4. **Rate limit errors**
   - The app includes rate limiting, but heavy usage may trigger limits
   - Wait a few minutes before retrying

### Performance Optimization
- The app screens a curated list of popular stocks for performance
- Results are limited to top 50 matches
- Caching can be implemented for frequently accessed data

## Customization

### Adding More Stocks
Edit the `popular_tickers` list in `app.py` to include additional stocks:

```python
popular_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN',  # Tech
    'JPM', 'BAC', 'WFC', 'C',         # Finance
    'XOM', 'CVX', 'COP', 'SLB',      # Energy
    # Add your preferred tickers here
]
```

### Adding New Filters
1. Add form field to `templates/index.html`
2. Update `collectCriteria()` function
3. Modify `passes_filters()` function in `app.py`

## License

This project is for educational and personal use. Please respect Polygon.io's terms of service and API usage limits.

## Support

For issues with the Polygon.io API, visit: https://polygon.io/docs
For application issues, check the console logs for detailed error messages.
