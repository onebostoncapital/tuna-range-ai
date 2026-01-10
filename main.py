# Master Rule Book: Main Orchestrator - Combines AI, On-Chain, and Technical signals
import pandas as pd
from ai_modules.forecasting import PriceForecaster
from ai_modules.sentiment import NewsAnalyzer
from core.technical import IndicatorSuite
from core.floor_logic import LiquidityFloorCalculator
from core.range_engine import RangeOptimizer

class TunaDecisionEngine:
    """
    The Boss Robot. 
    It calls every module and makes the final decision.
    """
    def __init__(self):
        self.forecaster = PriceForecaster()
        self.news_bot = NewsAnalyzer()
        self.math_bot = IndicatorSuite()
        self.floor_bot = LiquidityFloorCalculator()
        self.range_bot = RangeOptimizer()

    def run_strategy(self, price_data):
        # 1. Math Brain: Calculate indicators (MA20, RSI, etc.)
        df_with_indicators = self.math_bot.compute_all(price_data)
        
        # 2. Crystal Ball: Forecast future price
        prediction = self.forecaster.predict(price_data)
        
        # 3. Market Weather: Determine if Bullish or Bearish
        regime = self.math_bot.determine_regime(df_with_indicators, prediction)
        
        # 4. News Check: Get the Risk Factor
        news = self.news_bot.get_sentiment_risk()
        
        # 5. Safety Shield: Calculate the Floor
        current_price = price_data['close'].iloc[-1]
        indicators_now = df_with_indicators.iloc[-1]
        floor = self.floor_bot.compute_adjusted_floor(current_price, indicators_now, news['risk_factor'])
        
        # 6. Final Decision: Get the LP Range
        final_range = self.range_bot.calculate_lp_range(
            current_price, 
            indicators_now['atr14'], 
            regime, 
            floor
        )
        
        return {
            "current_price": current_price,
            "market_regime": regime,
            "news_risk": news['risk_factor'],
            "liquidity_floor": floor,
            "suggested_range": final_range,
            "recommendation": "LP_WAIT" if news['risk_factor'] > 0.8 else "LP_PROVIDE"
        }
