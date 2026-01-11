import pandas as pd

def compute_technical_indicators(df):
    """
    Calculates RSI, ATR, and MA20 and returns the MOST RECENT values as a dictionary.
    """
    # 1. 20-Day Moving Average
    df['MA20'] = df['y'].rolling(window=20).mean()
    
    # 2. RSI (14) - Simple implementation
    delta = df['y'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 3. ATR (Volatility)
    df['ATR'] = df['high'] - df['low']
    atr_val = df['ATR'].rolling(window=14).mean()

    # CRITICAL: Return a dictionary of the LATEST values, not the whole table
    latest_metrics = {
        'RSI': float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 50,
        'MA20': float(df['MA20'].iloc[-1]) if not pd.isna(df['MA20'].iloc[-1]) else float(df['y'].iloc[-1]),
        'ATR': float(atr_val.iloc[-1]) if not pd.isna(atr_val.iloc[-1]) else float(df['y'].iloc[-1] * 0.02)
    }
    
    return latest_metrics
