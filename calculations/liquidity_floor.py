# Master Rule Book: DeFiTuna Auto-Forecasting Engine (FIXED)
def get_strategy_details(current_price, indicators, principal=10000, leverage=2):
    # 1. Directional Bias
    rsi = indicators.get('RSI', 50)
    ma20 = indicators.get('MA20', current_price)
    
    # Rule: Bearish if RSI < 50 or Price < MA20
    is_bullish = rsi > 50 and current_price >= ma20
    bias = "BULLISH" if is_bullish else "BEARISH"
    
    # 2. Auto-Forecast Range (Dynamic ATR logic)
    atr = indicators.get('ATR', current_price * 0.03)
    
    if is_bullish:
        # Bullish: Range tilts UP, risk is BELOW ($36)
        low_bound = current_price - (atr * 1.5)
        high_bound = current_price + (atr * 3.0)
        liquidation_floor = current_price * 0.264 # Standard drop risk
    else:
        # Bearish: Range tilts DOWN, risk is ABOVE (Price Spike)
        low_bound = current_price - (atr * 3.0)
        high_bound = current_price + (atr * 1.5)
        # Bearish Rule: Liquidation occurs if price rises ~35-40% at 2x leverage
        liquidation_floor = current_price * 1.35 # Upper risk floor
    
    health_factor = abs((current_price - liquidation_floor) / current_price * 100)
    
    return {
        "bias": bias,
        "low": round(low_bound, 2),
        "high": round(high_bound, 2),
        "liquidation": round(liquidation_floor, 2),
        "total_exposure": principal * leverage,
        "safety_buffer": round(health_factor, 1)
    }
