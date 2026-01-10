# Master Rule Book: Final Orchestrator (The Command Center)
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Import our Specialist Modules
import config
from utils.logger import agent_logger
from apis.price_data import get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor
from ai_modules.ml_forecast import PriceForecaster
from ai_modules.nlp_sentiment import get_news_risk
from ai_modules.tail_risk import RiskSimulator
from ai_modules.anomaly_detection import AnomalyDetector
from ai_modules.rl_optimizer import RLOptimizer

class TunaAgent:
    def __init__(self):
        self.forecaster = PriceForecaster()
        self.risk_engine = RiskSimulator()
        self.anomaly_bot = AnomalyDetector()
        self.rl_agent = RLOptimizer()
        agent_logger.info("DeFiTuna Agent Initialized and ready for SoldUSDC.")

    def run_cycle(self):
        # 1. DATA INTAKE
        current_price = get_soldusdc_price()
        news_risk = get_news_risk()
        
        # Simulate historical data (Placeholder for actual API history)
        df = pd.DataFrame({
            'ds': pd.date_range(start='2024-01-01', periods=300, freq='H'),
            'y': np.random.normal(1.0, 0.005, 300).cumsum() + 10,
            'close': np.random.normal(1.0, 0.005, 300).cumsum() + 10,
            'high': np.random.normal(1.005, 0.005, 300).cumsum() + 10,
            'low': np.random.normal(0.995, 0.005, 300).cumsum() + 10,
            'volume': np.random.uniform(50000, 200000, 300)
        })

        # 2. BRAIN CALCULATIONS
        indicators = compute_technical_indicators(df)
        prediction = self.forecaster.predict(df)
        stress_test = self.risk_engine.run_simulation(current_price, indicators)
        
        # Determine Market Regime
        regime = "Range" if 40 < indicators['RSI'] < 60 else "Trend"
        
        # RL Optimization for Multiplier
        rl_multiplier = self.rl_agent.get_optimal_multiplier(regime, news_risk)
        
        # Anomaly Check
        anomalies = self.anomaly_bot.analyze_flow(df['volume'].iloc[-1], df['volume'].tolist())

        # 3. RANGE & FLOOR LOGIC
        base_floor = calculate_floor(current_price, indicators, news_risk)
        final_liquidity_floor = max(base_floor, stress_test['cvar_95_floor'])
        
        # Calculate LP Range (Skewed by Bias)
        range_width = (indicators['ATR'] * config.ATR_MULTIPLIER) * rl_multiplier
        if prediction['directional_bias'] == "Bullish":
            lower_range, upper_range = current_price - (range_width * 0.5), current_price + (range_width * 1.5)
        else:
            lower_range, upper_range = current_price - range_width, current_price + range_width

        # 4. FINAL OUTPUT
        output = {
            "timestamp": datetime.now().isoformat(),
            "asset": "SoldUSDC",
            "price": current_price,
            "analysis": {
                "regime": regime,
                "bias": prediction['directional_bias'],
                "confidence": f"{prediction['confidence_pct']}%",
                "news_risk_factor": news_risk
            },
            "strategy": {
                "liquidity_floor": final_liquidity_floor,
                "suggested_range": [round(lower_range, 4), round(upper_range, 4)],
                "rl_multiplier": rl_multiplier,
                "recommendation": "LP_PROVIDE" if not anomalies['is_anomaly'] and news_risk < 0.7 else "WAIT"
            },
            "alerts": anomalies['alerts']
        }

        return output

if __name__ == "__main__":
    agent = TunaAgent()
    result = agent.run_cycle()
    
    print(f"\n--- DEFITUNA AGENT REPORT ---")
    print(f"SoldUSDC Price: ${result['price']}")
    print(f"Market Bias: {result['analysis']['bias']} ({result['analysis']['confidence']} confidence)")
    print(f"Safety Floor: ${result['strategy']['liquidity_floor']}")
    print(f"Optimal Range: {result['strategy']['suggested_range']}")
    print(f"Final Decision: {result['strategy']['recommendation']}")
