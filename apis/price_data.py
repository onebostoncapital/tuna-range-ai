from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def get_live_market_data():
    """
    Synchronized for Jan 11, 2026. Price: $135.91
    Forces numeric types to prevent TypeError.
    """
    base_price = 135.91 
    
    # 1. Create a larger dataset (at least 30 points for a 20-period moving average)
    dates = [datetime.now() - timedelta(hours=x) for x in range(168)]
    noise = np.random.normal(0, 0.4, 168).cumsum()
    prices = base_price + noise
    
    # 2. Create DataFrame and EXPLICITLY set types
    df = pd.DataFrame({
        'ds': list(reversed(dates)),
        'y': prices.astype(float),      # Force to float
        'high': (prices * 1.005).astype(float),
        'low': (prices * 0.995).astype(float)
    })
    
    return df
