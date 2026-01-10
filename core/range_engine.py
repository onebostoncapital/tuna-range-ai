# Master Rule Book: Skewed LP Range (ATR x Multiplier) constrained by Liquidity Floor
class RangeOptimizer:
    """
    This is the robot's decision-maker for the SoldUSDC pool.
    It picks the Top and Bottom price for your money.
    """

    def calculate_lp_range(self, current_price, atr, regime, floor):
        # We start with a standard width (2.5 times the 'wiggle' of the price)
        multiplier = 2.5
        
        # We set our 'Skew' to 1.0 (balanced) as a starting point
        lower_skew = 1.0
        upper_skew = 1.0
        
        # Master Rule: Skew the range based on the Market Regime (Bullish/Bearish)
        if regime == "Bullish":
            # If bullish, we want to stay in the pool as price goes UP
            lower_skew = 0.8  # Pull the bottom up a bit
            upper_skew = 1.5  # Stretch the top way up!
        elif regime == "Bearish":
            # If bearish, we protect against the price going DOWN
            lower_skew = 1.5  # Stretch the bottom down
            upper_skew = 0.8  # Pull the top in
        elif regime == "High Volatility":
            # If it's crazy out there, we make the whole range wider
            multiplier = 4.0

        # Calculate the potential bounds
        lower_bound = current_price - (atr * multiplier * lower_skew)
        upper_bound = current_price + (atr * multiplier * upper_skew)
        
        # Master Rule: The range MUST be above our Safety Floor
        # This keeps us from losing money in 'bad neighborhoods'
        final_lower = max(lower_bound, floor)
        
        return {
            "lower_price": round(final_lower, 4),
            "upper_price": round(upper_bound, 4),
            "regime_used": regime
        }
