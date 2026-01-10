# Master Rule Book: Advanced AI Forecasting (ARIMA/Prophet)
import pandas as pd
from prophet import Prophet

class PriceForecaster:
    """
    This is the robot's crystal ball. 
    It looks at old prices to guess what might happen next.
    """
    def __init__(self):
        self.model = None

    def predict(self, price_history):
        # We turn the price list into a format the AI understands
        df = pd.DataFrame(price_history)
        df.columns = ['ds', 'y']
        
        # The robot starts guessing (training)
        self.model = Prophet(daily_seasonality=True)
        self.model.fit(df)
        
        # The robot looks 24 hours into the future
        future = self.model.make_future_dataframe(periods=24, freq='H')
        forecast = self.model.predict(future)
        
        # We take the most likely future price
        prediction = forecast['yhat'].iloc[-1]
        return round(prediction, 4)
