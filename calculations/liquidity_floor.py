# Master Rule Book: DeFiTuna Auto-Forecasting Engine
def get_strategy_details(current_price, indicators, principal=10000, leverage=2):
    # 1. Determine Directional Bias
    # Bullish if RSI > 50 and Price > MA20
    rsi = indicators.get('RSI', 50)
    ma20 = indicators.get('MA20', current_price)
    
    is_bullish = rsi > 50 and current_price >= ma20
    bias = "BULLISH" if is_bullish else "BEARISH"
    
    # 2. Auto-Forecast Range (Dynamic Based on Bias)
    atr = indicators.get('ATR', current_price * 0.03)
    
    if is_bullish:
        # Bullish: Shift range slightly higher to capture upside fees
        low_offset, high_offset = 1.0, 2.5
    else:
        # Bearish: Shift range lower to protect against price drops
        low_offset, high_offset = 2.5, 1.0
        
    forecast_low = current_price - (atr * low_offset)
    forecast_high = current_price + (atr * high_offset)
    
    # 3. Liquidation Floor (Fixed 2x Leveraged LP Math)
    # On DeFiTuna, 2x leverage liquidation is mathematically reached 
    # when the price drops by ~73.5% (approx 0.264 of entry)
    liquidation_floor = current_price * 0.264
    
    return {
        "bias": bias,
        "low": round(forecast_low, 2),
        "high": round(forecast_high, 2),
        "liquidation": round(liquidation_floor, 2),
        "total_value": principal * leverage,
        "health_factor": round((current_price - liquidation_floor) / current_price * 100, 1)
    }
