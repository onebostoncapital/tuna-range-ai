import streamlit as st
import plotly.graph_objects as go
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor

st.set_page_config(page_title="SoldUSDC AI", layout="wide")
st.title("🐟 SoldUSDC AI Risk Engine")

# Load Data
df = get_live_market_data()
price = get_soldusdc_price()
indicators = compute_technical_indicators(df)

# If indicators fail because of a data quirk, provide a safety default
if not indicators:
    indicators = {'ATR': price * 0.03, 'RSI': 50, 'MA20': price}

# Calculate Strategy
news_risk = 0.2 # Default low risk for now
floor = calculate_floor(price, indicators, news_risk)

# --- DISPLAY ---
col1, col2, col3 = st.columns(3)
col1.metric("Current Market Price", f"${price}")
col2.metric("AI Safety Floor", f"${floor}")
col3.metric("System Mode", "Live" if len(df) > 10 else "Simulated")

# Main Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price Trend", line=dict(color='#00FFA3')))
fig.add_trace(go.Scatter(x=df['ds'], y=[floor]*len(df), name="Risk Floor", line=dict(color='red', dash='dash')))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.success(f"Strategy: Maintain LP Range between ${floor} and ${round(price * 1.1, 2)}")
