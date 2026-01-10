# Master Rule Book: Liquidity Floor Calculation
# We use the max of structural (MA200) and volatility (ATR-based) floors.
import config

def calculate_floor(price, indicators, news_risk):
    """
    This is the safety shield for SoldUSDC.
    It tells us the price point we should not drop below.
    """
    # 1. Volatility Floor: Uses the ATR multiplier from our config
    vol_floor = price - (indicators['ATR'] * config.ATR_MULTIPLIER)
    
    # 2. Structural Floor: Uses the slow-moving MA200 (Long term support)
    struc_floor = indicators['MA200']
    
    # 3. Choose the strongest floor
    raw_floor = max(vol_floor, struc_floor)
    
    # 4. News Adjustment: If news_risk is high (near 1.0), the floor lowers to be safer
    # We use a 5% max adjustment as per our rules
    news_buffer = 1 - (news_risk * 0.05)
    adjusted_floor = raw_floor * news_buffer
    
    return round(adjusted_floor, 4)
