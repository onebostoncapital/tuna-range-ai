# Master Rule Book: Fixed Liquidity Floor Calculation
import pandas as pd

def calculate_floor(current_price, indicators, news_risk):
    """
    Expert Brain: Corrected Floor Logic for Stablecoins.
    Ensures the floor is relative to the ACTUAL asset price, not the trend proxy.
    """
    # 1. Structural Floor (Absolute Minimum)
    # For a stablecoin like SoldUSDC, it should never be 200.
    # It should be around 0.90 - 0.95 of its peg.
    structural_floor = current_price * 0.95
    
    # 2. Volatility Floor (Based on ATR)
    # If price is 1.0 and ATR is 0.02, floor is 0.98.
    # We cap the ATR impact so it doesn't create crazy numbers.
    atr_value = indicators.get('ATR', current_price * 0.05)
    
    # If ATR comes from SOL ($5.00), we normalize it to a percentage
    # relative to the current_price of the proxy.
    vol_impact = (atr_value / indicators.get('current_price', 150.0)) * current_price
    volatility_floor = current_price - (vol_impact * 2.0)
    
    # 3. Behavioral Floor (News Risk)
    # High news risk pushes the floor lower (protective)
    behavioral_floor = current_price * (1.0 - (news_risk * 0.1))

    # Master Rule: The Floor is the MAX (safest) of these three
    final_floor = max(structural_floor, volatility_floor, behavioral_floor)
    
    # Final Safety Check: Floor cannot be higher than 99% of current price
    if final_floor >= current_price:
        final_floor = current_price * 0.98

    return round(final_floor, 4)
