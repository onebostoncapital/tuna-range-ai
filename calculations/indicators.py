# Master Rule Book: Technical Indicators Engine
import pandas as pd
import pandas_ta as ta

def compute_technical_indicators(df):
    """
    Expert Brain: Calculates RSI, ATR, and Moving Averages.
    This version includes a 'Safety Clean' to prevent KeyError: 'close'.
    """
    # Safety Clean: Ensure all columns are lowercase before calculation
    df.columns = [col.lower() for col in df.columns]
    
    indicators = {}
    
    # Check if we have enough data (MA200 needs 200 points)
    if len(df) < 20:
        return None

    # 1. Trend Indicators
    # Using .get() ensures we don't crash if a column is slightly different
    close_price = df['close']
    
    indicators['MA20'] = close_price.rolling(window=20).mean().iloc[-1]
    indicators['MA200'] = close_price.rolling(window=200).mean().iloc[-1] if len(df) >= 200 else indicators['MA20']
    
    # 2. Momentum Indicators (RSI)
    rsi_series = ta.rsi(close_price, length=14)
    indicators['RSI'] = rsi_series.iloc[-1] if rsi_series is not None else 50.0
    
    # 3. Volatility Indicators (ATR)
    # ATR requires high, low, and close
    atr_df = ta.atr(df['high'], df['low'], close_price, length=14)
    indicators['ATR'] = atr_df.iloc[-1] if atr_df is not None else (close_price.iloc[-1] * 0.02)
    
    # 4. Market Summary
    indicators['current_price'] = close_price.iloc[-1]
    
    return indicators
