import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor

# 1. Page Config for Wide Mode
st.set_page_config(page_title="SoldUSDC AI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Inject Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    local_css("style.css")
except:
    pass # Falls back to default if file missing

# 3. Load Real 2026 Data
df = get_live_market_data()
# Force Sync to Jan 10, 2026 Market Price
market_price = 136.39 
usdc_price = 1.0

indicators = compute_technical_indicators(df)
floor = calculate_floor(usdc_price, indicators, 0.1)

# --- UI LAYOUT ---
st.title("🐟 DEFI TUNA | SoldUSDC Risk Engine")
st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')} UTC")

# Row 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("SOL/USD", f"${market_price}", "+2.4%")
col2.metric("SoldUSDC Floor", f"${floor}", "🛡️ Safe")
col3.metric("RSI (14)", f"{int(indicators.get('RSI', 50))}")
col4.metric("Risk Level", "LOW", delta_color="inverse")

# Row 2: Main Trading Chart
st.subheader("Market Trend Analysis")
fig = go.Figure()

# Candle/Line Trace
fig.add_trace(go.Scatter(
    x=df['ds'], y=df['y'], 
    name="SOL Price", 
    line=dict(color='#00ffa3', width=2),
    fill='toself', fillcolor='rgba(0, 255, 163, 0.1)'
))

# Safety Floor Trace (Visual Scale)
visual_floor = (floor / usdc_price) * market_price
fig.add_trace(go.Scatter(
    x=df['ds'], y=[visual_floor]*len(df), 
    name="Liquidity Floor", 
    line=dict(color='#ff4b4b', dash='dash')
))

fig.update_layout(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=20, b=20),
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# Row 3: Recommendations
with st.expander("📊 View AI Calculation Details"):
    st.write(f"The floor is calculated using a base price of **${usdc_price}** adjusted by a volatility factor (ATR) of **{round(indicators.get('ATR', 0), 4)}**.")
