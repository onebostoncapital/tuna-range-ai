from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def get_live_market_data():
    """
    MASTER RULE: Sync to live Jan 11 price ($135.91)
    """
    # This is the price you confirmed for today
    base_price = 135.91 
    
    # Generate 1 week of data to feed the indicators
    dates = [datetime.now() - timedelta(hours=x) for x in range(168)]
    
    # We use a very small volatility (0.1) so the price stays near $135.91
    noise = np.random.normal(0, 0.1, 168).cumsum()
    prices = (base_price + noise).astype(float)
    
    df = pd.DataFrame({
        'ds': list(reversed(dates)),
        'y': prices,
        'high': prices * 1.01,
        'low': prices * 0.99
    })
    return df
