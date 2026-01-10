import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# --- USER PARAMETERS ---
PRINCIPAL = 10000
LEVERAGE = 2
SOL_PRICE_2026 = 136.39  # Fixed Jan 10 price point

st.set_page_config(page_title="DeFiTuna Agent", layout="wide")

# Load Data & Brains
df = get_live_market_data()
indicators = compute_technical_indicators(df)
strategy = get_strategy_details(SOL_PRICE_2026, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
st.title("🛡️ DeFiTuna | AI Liquidity Orchestrator")
st.markdown(f"**Principal:** ${PRINCIPAL:,} | **Leverage:** {LEVERAGE}x | **Market Bias:** `{strategy['bias']}`")

# --- MASTER METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"${SOL_PRICE_2026}")
c2.metric("Auto-Range Forecast", f"${strategy['low']} - ${strategy['high']}")
c3.metric("Liquidation Floor", f"${strategy['liquidation']}", f"{strategy['safety_buffer']}% Buffer")
c4.metric("Total LP Exposure", f"${strategy['total_exposure']:,}")

# --- ANALYSIS CHART (FIXED SYNTAX) ---
fig = go.Figure()

# Price Trend Line
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Market Trend", line=dict(color='#00ffa3', width=2)))

# Liquidation Floor (Fixed Red Line)
fig.add_trace(go.Scatter(
    x=df['ds'], y=[strategy['liquidation']]*len(df),
    name="LIQUIDATION DANGER", line=dict(color='red', width=3, dash='dot')
))

# Forecast Range Glow (Fixed Area Logic)
x_vals = df['ds'].tolist()
y_upper = [strategy['high']] * len(df)
y_lower = [strategy['low']] * len(df)

fig.add_trace(go.Scatter(
    x=x_vals + x_vals[::-1],
    y=y_upper + y_lower[::-1],
    fill='toself',
    fillcolor='rgba(0, 255, 163, 0.05)',
    line=dict(color='rgba(0,0,0,0)'),
    name="Target LP Range",
    hoverinfo='skip'
))

fig.update_layout(template="plotly_dark", height=550, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- ACTION SUMMARY ---
if strategy['bias'] == "BULLISH":
    st.success(f"📈 **Bullish Bias Detected:** The AI suggests an asymmetrical range to capture upside. Suggested Range: **{strategy['low']} to {strategy['high']}**.")
else:
    st.warning(f"📉 **Bearish Bias Detected:** The AI suggests a protective range. Safety Floor at **${strategy['liquidation']}** is critical.")
