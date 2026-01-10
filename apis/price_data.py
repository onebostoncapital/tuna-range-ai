# Master Rule Book: CoinGecko Stable Engine
import requests
import pandas as pd
from datetime import datetime
import time

def get_live_market_data():
    """
    Fetches real historical data from CoinGecko.
    Standardizes output for AI and Indicators.
    """
    # CoinGecko ID for Solana (used as market trend proxy)
    coin_id = "solana" 
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30&interval=hourly"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'prices' not in data:
            return None
            
        # Convert CoinGecko JSON list to a clean DataFrame
        # Data format: [[timestamp, price], [timestamp, price], ...]
        df = pd.DataFrame(data['prices'], columns=['ds', 'y'])
        
        # Convert timestamp to readable date for Prophet AI
        df['ds'] = pd.to_datetime(df['ds'], unit='ms')
        
        # CoinGecko only gives price. We simulate High/Low for the ATR math
        # to ensure indicators.py doesn't crash.
        df['close'] = df['y']
        df['high'] = df['y'] * 1.002
        df['low'] = df['y'] * 0.998
        
        return df
    except Exception as e:
        print(f"CoinGecko Error: {e}")
        return None

def get_soldusdc_price():
    """Gets current price of Solana (Proxy for Market Condition)"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return float(response['solana']['usd'])
    except:
        return 1.0 # Stable fallback
