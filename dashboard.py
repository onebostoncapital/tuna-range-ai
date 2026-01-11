import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# --- 1. SETTINGS & AUTO-REFRESH ---
PRINCIPAL = 10000
LEVERAGE = 2

st.set_page_config(page_title="DeFiTuna AI Agent", layout="wide")

# This forces the browser to refresh the data every 30 seconds
st_autorefresh(interval=30 * 1000, key="pricerefresh")

# --- 2. DATA ENGINE ---
# We fetch the data fresh on every rerun (No st.cache allowed)
df = get_live_market_data()
indicators = compute_technical_indicators(df)

# Pull the absolute latest price from our 2026 data feed
current_market_price = float(df['y'].iloc[-1]) 

# Calculate strategy using the Master Rule Book logic
strategy = get_strategy_details(current_market_price, indicators, PRINCIPAL, LEVERAGE)

# --- 3. UI HEADER ---
st.title("🛡️ DeFiTuna | AI Strategy Engine")
st.markdown(f"**Principal:** ${PRINCIPAL:,} | **Leverage:** {LEVERAGE}x | **Live Market Status:** `{strategy['bias']}`")

# --- 4. MASTER METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("SOL Price", f"${current_market_price:,.2f}")
c2.metric("AI Auto-Range", f"${strategy['low']} - ${strategy['high']}")
# In BEARISH mode, this is the "Ceiling" risk
c3.metric("Liquidation Floor", f"${strategy['liquidation']}", f"{strategy['safety_buffer']}% Buffer")
c4.metric("Bias", strategy['bias'])

# --- 5. VISUALIZATION ---
fig = go.Figure()

# Price Trend
fig.add_trace(go.Scatter(
    x=df['ds'], y=df['y'], 
    name="SOL Price", 
    line=dict(color='#00ffa3', width=2)
))

# Target LP Range Shading
x_area = df['ds'].tolist() + df['ds'].tolist()[::-1]
y_upper = [strategy['high']] * len(df)
y_lower = [strategy['low']] * len(df)
fig.add_trace(go.Scatter(
    x=x_area, y=y_upper + y_lower[::-1],
    fill='toself', 
    fillcolor='rgba(0, 255, 163, 0.08)',
    line=dict(color='rgba(0,0,0,0)'), 
    name="AI Forecast Range"
))

# Liquidation Floor (Danger Line)
fig.add_trace(go.Scatter(
    x=df['ds'], y=[strategy['liquidation']] * len(df), 
    name="LIQUIDATION RISK", 
    line=dict(color='#ff4b4b', width=3, dash='dot')
))

fig.update_layout(
    template="plotly_dark", 
    height=550, 
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# --- 6. ACTION SUMMARY ---
if strategy['bias'] == "BEARISH":
    st.error(f"📉 **Bearish Strategy Active:** The Liquidation Floor is set at **${strategy['liquidation']}** (UPWARD risk). If SOL spikes to this level, your 2x leveraged SoldUSDC position will be liquidated.")
else:
    st.success(f"📈 **Bullish Strategy Active:** Liquidation Floor is at **${strategy['liquidation']}** (DOWNWARD risk). Safety buffer is currently {strategy['safety_buffer']}%.")

st.info(f"💡 **AI Recommendation:** Set your concentrated liquidity pool range to **{strategy['low']} - {strategy['high']}** to maximize fee collection based on current {strategy['bias']} volatility.")
