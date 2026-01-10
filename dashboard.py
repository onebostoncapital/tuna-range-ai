# Master Rule Book: Fixed Dashboard (NameError Fix)
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime  # <--- CRITICAL FIX FOR NAMEERROR
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor

st.set_page_config(page_title="SoldUSDC Strategy", layout="wide")
st.title("🛡️ SoldUSDC Risk Engine (Live: Jan 2026)")

# Load Live 2026 Data
df = get_live_market_data()
market_price = get_soldusdc_price() # Should now reflect ~$136.39
usdc_price = 1.0 # Target peg for SoldUSDC

indicators = compute_technical_indicators(df)

# Logic: Use Market volatility to set the USDC floor
# If indicators are empty, provide safety defaults
if not indicators:
    indicators = {'ATR': market_price * 0.02, 'current_price': market_price}

floor = calculate_floor(usdc_price, indicators, 0.2)

# --- DISPLAY ---
c1, c2, c3 = st.columns(3)
c1.metric("SOL Market Trend", f"${market_price}")
c2.metric("SoldUSDC Safety Floor", f"${floor}")
c3.metric("System Date", datetime.now().strftime("%Y-%m-%d"))

# Main Analysis Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="SOL Trend", line=dict(color='#00FFA3')))
# The floor is relative to USDC ($1.0), so we multiply for visual scaling on the SOL chart
visual_floor = (floor / usdc_price) * market_price 
fig.add_trace(go.Scatter(x=df['ds'], y=[visual_floor]*len(df), name="Scaled Risk Floor", line=dict(color='red', dash='dash')))

fig.update_layout(template="plotly_dark", title="Market Trend vs. Structural Risk Floor")
st.plotly_chart(fig, use_container_width=True)

st.info(f"Analysis: SOL is trading at ${market_price}. Your SoldUSDC floor is set to ${floor} based on current volatility.")
