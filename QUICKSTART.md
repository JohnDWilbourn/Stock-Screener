# Quick Start Guide - Stock Screener

## 🚀 Get Started in 3 Steps

### Step 1: Get Your Polygon.io API Key
1. Go to [Polygon.io](https://polygon.io) 
2. Sign up for the **$29 Starter tier** (or higher)
3. Get your API key from the dashboard

### Step 2: Configure Your API Key
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and replace `your_polygon_api_key_here` with your actual API key

### Step 3: Run the Application
```bash
python setup.py
```

That's it! The application will be available at `http://localhost:5000`

---

## 📊 Quick Screening Examples

### Find Today's Top Gainers
- **Min Change %**: 5
- **Min Volume**: 1000000
- **Sort by**: Change %

### Find Oversold Stocks
- **Max RSI**: 30
- **Min Market Cap**: Large Cap ($10B+)
- **Sort by**: RSI

### Find High Volume Breakouts
- **Min Volume**: 5000000
- **Price above 50 SMA**: ✓
- **Min Change %**: 3
- **Sort by**: Volume

---

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

1. **Create virtual environment:**
   ```bash
   python3 -m venv stock_screener_env
   source stock_screener_env/bin/activate  # On Windows: stock_screener_env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

---

## 📱 Using the Application

1. **Set Filters**: Use the form to set your screening criteria
2. **Screen Stocks**: Click "Screen Stocks" to run the analysis
3. **View Results**: Results appear in a sortable table
4. **Stock Details**: Click any stock row to see detailed information
5. **Export/Save**: Results can be sorted and analyzed directly in the interface

---

## 🆘 Troubleshooting

### Application won't start?
- Check that your API key is correctly set in `.env`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### No results found?
- Try broader filter criteria
- Some technical indicators may not be available for all stocks

### Slow performance?
- The app processes multiple API calls - initial requests may take 30-60 seconds
- Results are cached for better performance

---

## 📞 Support

- **API Issues**: Check [Polygon.io documentation](https://polygon.io/docs)
- **Rate Limits**: The app includes built-in rate limiting
- **Feature Requests**: See the main README for customization options