import streamlit as st
import plotly.graph_objects as go
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# Parameters
PRINCIPAL = 10000
LEVERAGE = 2
SOL_PRICE = 136.39 # Jan 10, 2026

st.set_page_config(page_title="DeFiTuna AI Agent", layout="wide")

# Load Brains
df = get_live_market_data()
indicators = compute_technical_indicators(df)
strategy = get_strategy_details(SOL_PRICE, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
st.title("🛡️ DeFiTuna | AI Strategy Engine")
st.markdown(f"**Status:** {strategy['bias']} Strategy Active | **Capital:** ${PRINCIPAL:,}")

# --- METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"${SOL_PRICE}")
c2.metric("AI Auto-Range", f"${strategy['low']} - ${strategy['high']}")
c3.metric("Liquidation Floor", f"${strategy['liquidation']}", f"{strategy['safety_buffer']}% Buffer")
c4.metric("Strategy Bias", strategy['bias'])

# --- CHARTING ---
fig = go.Figure()

# Market Trend
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="SOL Price", line=dict(color='#00ffa3')))

# Fixed Area Logic for Range Shading
x_vals = df['ds'].tolist()
y_upper = [strategy['high']] * len(df)
y_lower = [strategy['low']] * len(df)

fig.add_trace(go.Scatter(
    x=x_vals + x_vals[::-1],
    y=y_upper + y_lower[::-1],
    fill='toself', fillcolor='rgba(0, 255, 163, 0.05)',
    line=dict(color='rgba(0,0,0,0)'), name="Target LP Range"
))

# Liquidation Floor (Dynamic placement based on Bias)
fig.add_trace(go.Scatter(
    x=df['ds'], y=[strategy['liquidation']]*len(df),
    name="LIQUIDATION RISK", line=dict(color='red', width=3, dash='dot')
))

fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- MASTER RULE BOOK NOTIFICATION ---
if strategy['bias'] == "BEARISH":
    st.error(f"⚠️ **Bearish Alert:** Liquidation Floor is now at **${strategy['liquidation']}**. A price spike above this level will liquidate your leveraged SoldUSDC position.")
else:
    st.success(f"✅ **Bullish Alert:** Liquidation Floor is at **${strategy['liquidation']}**. You are protected against price drops up to {strategy['safety_buffer']}%.")
