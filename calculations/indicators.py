# Master Rule Book: Crash-Proof Indicators Engine
import pandas as pd
import pandas_ta as ta

def compute_technical_indicators(df):
    """
    Expert Brain: Calculates RSI, ATR, and Moving Averages.
    Standardizes all column names to lowercase to prevent KeyError.
    """
    if df is None or df.empty:
        return None
        
    # FORCE everything to lowercase immediately
    df.columns = [col.lower() for col in df.columns]
    
    # Check if we have enough data (MA20 needs 20 points)
    if len(df) < 20:
        return None

    indicators = {}
    
    # Standard columns used in DeFi math
    try:
        close_price = df['close']
        
        # 1. Trend Indicators
        indicators['MA20'] = close_price.rolling(window=20).mean().iloc[-1]
        indicators['MA200'] = close_price.rolling(window=200).mean().iloc[-1] if len(df) >= 200 else indicators['MA20']
        
        # 2. Momentum (RSI)
        rsi_series = ta.rsi(close_price, length=14)
        indicators['RSI'] = rsi_series.iloc[-1] if rsi_series is not None else 50.0
        
        # 3. Volatility (ATR)
        atr_df = ta.atr(df['high'], df['low'], close_price, length=14)
        indicators['ATR'] = atr_df.iloc[-1] if atr_df is not None else (close_price.iloc[-1] * 0.02)
        
        # 4. Market Summary
        indicators['current_price'] = close_price.iloc[-1]
        
        return indicators
    except Exception as e:
        print(f"Calculation Error: {e}")
        return None
