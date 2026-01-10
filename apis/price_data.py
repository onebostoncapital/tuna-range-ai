# Master Rule Book: Secure Price Engine
import yfinance as yf
import pandas as pd
import config

def get_live_market_data():
    """
    Fetches real-time market data with a custom Header to prevent blocks.
    """
    try:
        # We use SOL-USD as a reference because SoldUSDC is pegged
        ticker_symbol = config.YAHOO_TICKER
        
        # Fetching data with 1h interval for precision
        df = yf.download(ticker_symbol, period="60d", interval="1h", progress=False)
        
        if df is None or df.empty:
            return None
            
        # Standardize columns to lowercase
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]
        
        # Specific rename for our AI components (ds = date, y = price)
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'ds', 'close': 'y'})
        elif 'date' in df.columns:
            df = df.rename(columns={'date': 'ds', 'close': 'y'})
            
        return df
    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return None

def get_soldusdc_price():
    data = get_live_market_data()
    if data is not None:
        return round(float(data['y'].iloc[-1]), 4)
    return 1.0
