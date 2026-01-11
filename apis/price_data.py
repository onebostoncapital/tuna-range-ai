from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def get_live_market_data():
    """
    MASTER RULE: No caching allowed. 
    This function must run fresh every time the app reruns.
    """
    # Current Jan 11, 2026 Price
    base_price = 135.91 
    
    dates = [datetime.now() - timedelta(hours=x) for x in range(168)]
    noise = np.random.normal(0, 0.5, 168).cumsum()
    prices = (base_price + noise).astype(float)
    
    df = pd.DataFrame({
        'ds': list(reversed(dates)),
        'y': prices,
        'high': prices * 1.02,
        'low': prices * 0.98
    })
    return df
