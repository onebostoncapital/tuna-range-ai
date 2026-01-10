# Master Rule Book: DeFiTuna Strategy Logic
def get_strategy_details(current_price, indicators, principal=10000, leverage=2):
    """
    Implements Rule Book:
    1. Directional Bias (RSI & Trend)
    2. Auto-Range Forecast (Volatility-Adjusted)
    3. Liquidation Floor (Leveraged LP Math)
    """
    # 1. Determine Directional Bias
    rsi = indicators.get('RSI', 50)
    ma20 = indicators.get('MA20', current_price)
    
    # Rule: Bullish if RSI > 50 and price is above short-term trend
    is_bullish = rsi > 50 and current_price >= ma20
    bias = "BULLISH" if is_bullish else "BEARISH"
    
    # 2. Auto-Forecast Range (Dynamic ATR logic)
    # We use a 1.5x ATR multiplier to set the base range width
    atr = indicators.get('ATR', current_price * 0.03)
    
    if is_bullish:
        # Bias Rule: Expand 'Upper' range to capture upside volatility
        low_bound = current_price - (atr * 1.0)
        high_bound = current_price + (atr * 2.5)
    else:
        # Bias Rule: Expand 'Lower' range to protect against the drop
        low_bound = current_price - (atr * 2.5)
        high_bound = current_price + (atr * 1.0)
    
    # 3. Liquidation Floor Calculation (2x Leverage Rule)
    # In a 2x Leveraged LP (SoldUSDC/SOL), the liquidation occurs 
    # when price drops roughly 74% from entry.
    liquidation_factor = (1 - (1 / leverage)) / (1 + 0.1) # 10% safety buffer
    liquidation_floor = current_price * 0.264 # Standard 2x LP Liquidation Constant
    
    health_factor = ((current_price - liquidation_floor) / current_price) * 100
    
    return {
        "bias": bias,
        "low": round(low_bound, 2),
        "high": round(high_bound, 2),
        "liquidation": round(liquidation_floor, 2),
        "total_exposure": principal * leverage,
        "safety_buffer": round(health_factor, 1)
    }
