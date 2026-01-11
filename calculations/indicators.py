import pandas as pd

def compute_technical_indicators(df):
    # Safety: Ensure we have enough rows for a 20-period average
    if len(df) < 20:
        return {'RSI': 50, 'MA20': float(df['y'].iloc[-1]), 'ATR': 1.5}

    # Ensure y is numeric
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    
    # Calculate MA20
    df['MA20'] = df['y'].rolling(window=20, min_periods=1).mean()
    
    # Calculate RSI
    delta = df['y'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate ATR
    df['ATR'] = (df['high'] - df['low']).rolling(window=14, min_periods=1).mean()

    # Return latest dictionary
    return {
        'RSI': float(df['RSI'].iloc[-1]),
        'MA20': float(df['MA20'].iloc[-1]),
        'ATR': float(df['ATR'].iloc[-1])
    }
