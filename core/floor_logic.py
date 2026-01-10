# Master Rule Book: Liquidity Floor = Max(Structural, Volatility, Behavioral) adjusted by News Risk
import numpy as np

class LiquidityFloorCalculator:
    """
    This is the robot's Safety Shield. 
    It calculates the 'Floor' - the price we should not go below.
    """

    def compute_adjusted_floor(self, current_price, indicators, news_risk_factor):
        # 1. Structural Floor: Look at old 'High Volume' areas or Support
        # We use the MA200 as a strong structural floor
        structural_floor = indicators['ma200']

        # 2. Volatility Floor: Price minus (ATR x Multiplier)
        # ATR tells us how much the price 'wiggles'. We stay below the wiggles.
        volatility_floor = current_price - (indicators['atr14'] * 2.5)

        # 3. Behavioral Floor: Looking at what 'Whales' are doing
        # For now, we use the VWAP (the price where most people traded)
        behavioral_floor = indicators['vwap']

        # Master Rule: Pick the strongest (highest) of these floors
        raw_floor = max(structural_floor, volatility_floor, behavioral_floor)

        # Master Rule: Adjust by the News Risk Factor
        # If news is scary (Risk = 1.0), we lower our floor to be extra safe
        # If news is happy (Risk = 0.0), we keep our floor firm
        news_adjustment = 1 - (news_risk_factor * 0.05) 
        adjusted_floor = raw_floor * news_adjustment

        return round(adjusted_floor, 4)
