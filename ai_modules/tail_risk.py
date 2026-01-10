# Master Rule Book: Tail-Risk Simulation (Monte Carlo & CVaR)
import numpy as np
import pandas as pd

class RiskSimulator:
    """
    Expert Brain: Simulates 10,000 futures to calculate 'Worst-Case' scenarios.
    Satisfies Requirement: Conditional VaR (CVaR) and Monte Carlo.
    """
    def __init__(self, num_simulations=10000, time_horizon=24):
        self.num_simulations = num_simulations
        self.time_horizon = time_horizon # 24 hours

    def run_simulation(self, current_price, indicators):
        # 1. Get volatility from ATR (normalized to percentage)
        volatility = (indicators['ATR'] / current_price)
        
        # 2. Monte Carlo: Generate 10,000 random price paths
        # formula: Price * exp(random_walk)
        daily_returns = np.random.normal(0, volatility, self.num_simulations)
        simulated_prices = current_price * np.exp(daily_returns)
        
        # 3. Calculate Value at Risk (VaR) at 95% confidence
        # This is the 'Bad Day' threshold
        var_95 = np.percentile(simulated_prices, 5)
        
        # 4. Calculate Conditional VaR (CVaR) - The 'Tail Risk'
        # This is the average price in the absolute worst 5% of cases
        tail_losses = simulated_prices[simulated_prices <= var_95]
        cvar_95 = np.mean(tail_losses)
        
        # 5. Determine Tail Risk Score
        # How far is the 'worst case' from the current price?
        risk_pct = (current_price - cvar_95) / current_price
        
        return {
            "var_95": round(var_95, 4),
            "cvar_95_floor": round(cvar_95, 4), # This becomes a new 'Behavioral Floor'
            "tail_risk_severity": "High" if risk_pct > 0.05 else "Normal",
            "max_simulated_drawdown": round(risk_pct * 100, 2)
        }
