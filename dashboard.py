import streamlit as st
import plotly.graph_objects as go
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor

st.set_page_config(page_title="SoldUSDC Strategy", layout="wide")
st.title("🛡️ SoldUSDC Risk Engine (Jan 2026)")

# Load Live 2026 Data
df = get_live_market_data()
market_price = get_soldusdc_price() # This is the SOL Price ($135.87)
usdc_price = 1.0 # This is your LP asset

indicators = compute_technical_indicators(df)
# Logic: Use Market volatility to set the USDC floor
floor = calculate_floor(usdc_price, indicators, 0.2)

# --- DISPLAY ---
c1, c2, c3 = st.columns(3)
c1.metric("SOL Market Trend", f"${market_price}")
c2.metric("SoldUSDC Safety Floor", f"${floor}")
c3.metric("System Date", datetime.now().strftime("%Y-%m-%d"))
