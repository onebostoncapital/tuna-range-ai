import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# Configuration
PRINCIPAL = 10000
LEVERAGE = 2
MARKET_PRICE = 136.39

st.set_page_config(page_title="DeFiTuna AI Agent", layout="wide")

# Load CSS & Data
df = get_live_market_data()
indicators = compute_technical_indicators(df)
strategy = get_strategy_details(MARKET_PRICE, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
st.title("🛡️ DeFiTuna | Automated Liquidity Agent")
st.markdown(f"**Principal:** ${PRINCIPAL:,} | **Leverage:** {LEVERAGE}x | **Bias:** `{strategy['bias']}`")

# --- TOP ROW: MASTER RULES ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("SOL Market Price", f"${MARKET_PRICE}")
c2.metric("Auto-Forecast Range", f"${strategy['low']} - ${strategy['high']}")
c3.metric("Liquidation Floor", f"${strategy['liquidation']}", f"{strategy['health_factor']}% Buffer")
c4.metric("Active Leverage", f"{LEVERAGE}x")

# --- CHARTING ---
fig = go.Figure()

# Market Price
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="SOL Trend", line=dict(color='#00ffa3', width=2)))

# Liquidation Floor Area (Red Zone)
fig.add_trace(go.Scatter(
    x=df['ds'], y=[strategy['liquidation']]*len(df),
    name="LIQUIDATION FLOOR", line=dict(color='red', width=4, dash='dot')
))

# Forecast Range Area (Glow Zone)
x_area = df['ds'].tolist() + df['ds'].tolist()[::-1]
y_area = [strategy['high']]*len(df) + [strategy['low']]*len(df)[::-1]
fig.add_trace(go.Scatter(x=x_area, y=y_area, fill='toself', fillcolor='rgba(0, 255, 163, 0.05)', line=dict(color='rgba(0,0,0,0)'), name="Target LP Range"))

fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

# --- RULE BOOK FOOTER ---
st.warning(f"🚨 **Liquidation Alert:** If SOL hits the **${strategy['liquidation']}** floor, your **${PRINCIPAL:,}** margin will be lost. Current safety buffer is **{strategy['health_factor']}%**.")
