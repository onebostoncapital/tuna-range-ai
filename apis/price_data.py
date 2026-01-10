# Master Rule Book: Real-Time Price Engine
import yfinance as yf
import pandas as pd
import config

def get_live_market_data():
    """
    Fetches 60 days of hourly data. 
    Hourly data is better for SoldUSDC range fine-tuning.
    """
    try:
        # We fetch 60 days to ensure MA200 has enough points
        ticker = yf.Ticker(config.YAHOO_TICKER)
        df = ticker.history(period="60d", interval="1h")
        
        if df.empty:
            return None
            
        # Standardize columns to lowercase immediately
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]
        
        # Prophet AI specifically needs 'ds' and 'y'
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'ds', 'close': 'y'})
        elif 'date' in df.columns:
            df = df.rename(columns={'date': 'ds', 'close': 'y'})
            
        return df
    except Exception as e:
        print(f"Error fetching live data: {e}")
        return None

def get_soldusdc_price():
    data = get_live_market_data()
    if data is not None:
        return round(data['y'].iloc[-1], 4)
    return 1.0
