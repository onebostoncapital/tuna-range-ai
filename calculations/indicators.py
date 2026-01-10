import pandas as pd

def compute_technical_indicators(df):
    """
    Master Rule: Calculate MA20, MA200, RSI, ATR, and ADX
    """
    indicators = {}
    # Moving Averages
    indicators['MA20'] = df['close'].rolling(window=20).mean().iloc[-1]
    indicators['MA200'] = df['close'].rolling(window=200).mean().iloc[-1]
    
    # RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators['RSI'] = 100 - (100 / (1 + rs.iloc[-1]))
    
    # ATR (Average True Range)
    indicators['ATR'] = (df['high'] - df['low']).rolling(window=14).mean().iloc[-1]
    
    return indicators
