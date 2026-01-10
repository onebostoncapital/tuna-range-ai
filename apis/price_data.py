# Master Rule Book: Real-Time Price Engine
import yfinance as yf
import pandas as pd
import config

def get_live_market_data():
    """
    Fetches real historical and live data from Yahoo Finance.
    Provides Open, High, Low, Close, and Volume.
    """
    try:
        # Fetch last 60 days of hourly data to ensure indicators have enough points
        ticker = yf.Ticker(config.YAHOO_TICKER)
        df = ticker.history(period="60d", interval="1h")
        
        if df.empty:
            return None
            
        # Clean the data for our Math Brain
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]
        
        # Rename columns to match our strategy requirements
        # ds = datestamp, y = price (required by Prophet AI)
        df = df.rename(columns={'datetime': 'ds', 'close': 'y'})
        
        return df
    except Exception as e:
        print(f"Error fetching live data: {e}")
        return None

def get_soldusdc_price():
    """
    Gets the most recent single price point.
    """
    data = get_live_market_data()
    if data is not None:
        return round(data['y'].iloc[-1], 4)
    return 1.0 # Fallback for stablecoin
