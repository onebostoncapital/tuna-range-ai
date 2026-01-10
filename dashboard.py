import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# Configuration
PRINCIPAL = 10000
LEVERAGE = 2
MARKET_PRICE = 136.39 # Live Jan 10, 2026 Price

st.set_page_config(page_title="DeFiTuna AI", layout="wide")

# Load Data
df = get_live_market_data()
indicators = compute_technical_indicators(df)
strategy = get_strategy_details(MARKET_PRICE, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
st.title("🐟 DeFiTuna | AI Liquidity Agent")
st.markdown(f"**Strategy:** SoldUSDC/SOL Loop | **Capital:** ${PRINCIPAL:,} | **Leverage:** {LEVERAGE}x")

# --- TOP ROW: STRATEGY METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("SOL Market Price", f"${MARKET_PRICE}")
c2.metric("Forecast Range", f"${strategy['low']} - ${strategy['high']}")
c3.metric("Liquidation Level", f"${strategy['liquidation']}", delta="-75%", delta_color="inverse")
c4.metric("Total LP Exposure", f"${strategy['total_value']:,}")

# --- MAIN CHART WITH FORECAST SHADING ---
fig = go.Figure()

# Price Line
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="SOL Trend", line=dict(color='#00ffa3')))

# Forecast Range (Shaded Area)
fig.add_trace(go.Scatter(
    x=df['ds'].tolist() + df['ds'].tolist()[::-1],
    y=[strategy['high']]*len(df) + [strategy['low']]*len(df)[::-1],
    fill='toself', fillcolor='rgba(0, 255, 163, 0.1)',
    line=dict(color='rgba(255,255,255,0)'), name="AI Forecast Range"
))

# Liquidation Line (Red)
fig.add_trace(go.Scatter(x=df['ds'], y=[strategy['liquidation']]*len(df), 
                         name="LIQUIDATION LEVEL", line=dict(color='red', width=3, dash='dot')))

fig.update_layout(template="plotly_dark", height=600, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- ACTION PANEL ---
st.success(f"✅ **AI Recommendation:** Set your LP Range between **${strategy['low']}** and **${strategy['high']}**. Your liquidation safety buffer is **${round(MARKET_PRICE - strategy['liquidation'], 2)}**.")
