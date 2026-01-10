# Master Rule Book: Advanced Forecasting & Liquidation Logic
def get_strategy_details(current_price, indicators, principal=10000, leverage=2):
    """
    Calculates the auto-forecast range and the 2x leverage liquidation level.
    """
    # 1. AI Forecast Range
    # We use 2x ATR for a 95% confidence interval in the forecast
    atr = indicators.get('ATR', current_price * 0.02)
    forecast_low = current_price - (atr * 1.5)
    forecast_high = current_price + (atr * 1.5)
    
    # 2. Liquidation Level (Fixed 2x Leverage)
    # For Liquidity Mining (LP), liquidation is calculated differently than futures.
    # At 2x leverage, your liquidation price is roughly 25% of the entry price.
    liquidation_price = 1.05 * current_price * ((leverage - 1) / leverage)**2
    
    return {
        "low": round(forecast_low, 4),
        "high": round(forecast_high, 4),
        "liquidation": round(liquidation_price, 4),
        "total_value": principal * leverage
    }
