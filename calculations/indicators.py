# Master Rule Book: Indicators (MA, RSI, ADX, ATR, VWAP)
import pandas as pd

class IndicatorSuite:
    def compute_all(self, df):
        # MA20 & MA200 (The Trend)
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma200'] = df['close'].rolling(window=200).mean()

        # RSI14 (Overbought/Oversold)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['rsi14'] = 100 - (100 / (1 + (gain / loss)))

        # ATR14 (Volatility/Jumpiness)
        df['atr14'] = (df['high'] - df['low']).rolling(window=14).mean()

        # VWAP (Volume Weighted Average Price)
        df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
        
        return df
