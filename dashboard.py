import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from apis.price_data import get_live_market_data
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import get_strategy_details

# --- SETTINGS ---
PRINCIPAL = 10000
LEVERAGE = 2

st.set_page_config(page_title="DeFiTuna AI Agent", layout="wide")

# Trigger refresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="pricerefresh")

# --- DATA ENGINE ---
df = get_live_market_data()

# Safety Check: If data failed, show warning but don't crash
if df is None or df.empty:
    st.error("⚠️ Data Engine is offline. Please check your API connection.")
    st.stop()

# Calculate Indicators and Strategy
indicators = compute_technical_indicators(df)
current_price = float(df['y'].iloc[-1])
strategy = get_strategy_details(current_price, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🛡️ DeFiTuna | AI Strategy Engine")
with c2:
    st.caption(f"🕒 **Last Pulse:** {datetime.now().strftime('%H:%M:%S')}")
    st.caption(f"💰 **SOL Current:** ${current_price:,.2f}")

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Live Price", f"${current_price:,.2f}")
m2.metric("AI Auto-Range", f"${strategy['low']} - ${strategy['high']}")
m3.metric("Liquidation Risk", f"${strategy['liquidation']}", f"{strategy['safety_buffer']}% Buffer")
m4.metric("Bias", strategy['bias'])

# --- CHART ---
fig = go.Figure()

# Price Path
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price", line=dict(color='#00ffa3', width=2)))

# Liquidation Danger Line (Ceiling for Bearish, Floor for Bullish)
fig.add_trace(go.Scatter(x=df['ds'], y=[strategy['liquidation']] * len(df), 
                         name="LIQUIDATION DANGER", line=dict(color='#ff4b4b', width=3, dash='dot')))

fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- STATUS MESSAGES ---
if strategy['bias'] == "BEARISH":
    st.error(f"📉 **Bearish Mode Active:** Risk is on the **UPWARD** side. Watch for price spikes near **${strategy['liquidation']}**.")
else:
    st.success(f"📈 **Bullish Mode Active:** Risk is on the **DOWNWARD** side. Protection floor is at **${strategy['liquidation']}**.")
