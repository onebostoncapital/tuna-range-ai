# Master Rule Book: Technical Indicators (MA, RSI, ADX, ATR, VWAP)
import pandas as pd
import numpy as np

class IndicatorSuite:
    """
    This is the robot's math brain. 
    It turns messy price numbers into clear signals.
    """

    def compute_all(self, df):
        # Master Rule: We need MA20 and MA200 to see the trend
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma200'] = df['close'].rolling(window=200).mean()

        # Master Rule: RSI14 (Are people over-buying?)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi14'] = 100 - (100 / (1 + rs))

        # Master Rule: ATR14 (How 'jumpy' is the price?)
        df['high_low'] = df['high'] - df['low']
        df['atr14'] = df['high_low'].rolling(window=14).mean()

        # Master Rule: VWAP (The 'Fair' Price based on volume)
        df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()

        return df

    def determine_regime(self, df, ml_forecast):
        """
        Master Rule: Determine Market Regime (Bullish, Bearish, Range, High Volatility)
        """
        last_price = df['close'].iloc[-1]
        ma20 = df['ma20'].iloc[-1]
        atr = df['atr14'].iloc[-1]
        
        # Simple logic for the robot to decide the 'weather' of the market
        if last_price > ma20 and ml_forecast > last_price:
            return "Bullish"
        elif last_price < ma20 and ml_forecast < last_price:
            return "Bearish"
        elif atr > (last_price * 0.05): # If price jumps more than 5%
            return "High Volatility"
        else:
            return "Range Bound"
