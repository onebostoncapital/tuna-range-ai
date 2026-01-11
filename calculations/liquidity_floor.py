# Master Rule Book: Fixed Strategy Logic
def get_strategy_details(current_price, indicators, principal=10000, leverage=2):
    # indicators is now a dictionary, so .get() will work!
    rsi = indicators.get('RSI', 50)
    ma20 = indicators.get('MA20', current_price)
    
    # Bias Logic
    is_bullish = rsi > 50 and current_price >= ma20
    bias = "BULLISH" if is_bullish else "BEARISH"
    
    # Range & Liquidation
    atr = indicators.get('ATR', current_price * 0.03)
    
    if bias == "BULLISH":
        low_bound, high_bound = current_price - (atr * 1.5), current_price + (atr * 3.0)
        liquidation_floor = current_price * 0.264
    else:
        low_bound, high_bound = current_price - (atr * 3.0), current_price + (atr * 1.5)
        liquidation_floor = current_price * 1.35 # Risk is above
    
    return {
        "bias": bias,
        "low": round(low_bound, 2),
        "high": round(high_bound, 2),
        "liquidation": round(liquidation_floor, 2),
        "total_exposure": principal * leverage,
        "safety_buffer": round(abs((current_price - liquidation_floor) / current_price * 100), 1)
    }
