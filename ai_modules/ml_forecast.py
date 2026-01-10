# Master Rule Book: ML Forecasting (Prophet + ARIMA)
import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

class PriceForecaster:
    """
    Advanced AI Brain: Combines Prophet (Trends) and ARIMA (Short-term moves).
    """
    def __init__(self):
        self.confidence = 0.0
        self.bias = "Neutral"

    def predict(self, df):
        # We need the 'close' price history
        series = df['close']
        
        # --- 1. Prophet Model (The Trend Finder) ---
        prophet_df = df[['ds', 'y']] # ds is date, y is price
        m = Prophet(daily_seasonality=True, interval_width=0.95)
        m.fit(prophet_df)
        future = m.make_future_dataframe(periods=6, freq='H')
        forecast = m.predict(future)
        prophet_pred = forecast['yhat'].iloc[-1]

        # --- 2. ARIMA Model (The Momentum Finder) ---
        # We look at the last 100 hours to see the 'swing'
        arima_model = ARIMA(series, order=(5,1,0))
        arima_result = arima_model.fit()
        arima_pred = arima_result.forecast(steps=1)[0]

        # --- 3. Combine Results (Ensemble) ---
        avg_prediction = (prophet_pred + arima_pred) / 2
        current_price = series.iloc[-1]
        
        # Calculate Directional Bias
        if avg_prediction > current_price * 1.005:
            self.bias = "Bullish"
        elif avg_prediction < current_price * 0.995:
            self.bias = "Bearish"
        else:
            self.bias = "Range"

        # Master Rule: Generate Confidence Percentage
        # If both models agree, confidence is high!
        agreement = 1 - abs(prophet_pred - arima_pred) / current_price
        self.confidence = round(agreement * 100, 2)

        return {
            "predicted_price": round(avg_prediction, 4),
            "directional_bias": self.bias,
            "confidence_pct": self.confidence
        }
