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

# Trigger refresh every 10 seconds to eliminate lag feel
count = st_autorefresh(interval=10 * 1000, key="pricerefresh")

# --- DATA ENGINE ---
df = get_live_market_data()
indicators = compute_technical_indicators(df)
current_price = float(df['y'].iloc[-1])
strategy = get_strategy_details(current_price, indicators, PRINCIPAL, LEVERAGE)

# --- UI HEADER ---
c_title, c_status = st.columns([3, 1])
with c_title:
    st.title("🛡️ DeFiTuna | AI Strategy Engine")
with c_status:
    st.write("") # Padding
    st.caption(f"🕒 **Last Pulse:** {datetime.now().strftime('%H:%M:%S')}")
    st.caption(f"🔄 **Refreshes:** {count}")

st.markdown(f"**Principal:** ${PRINCIPAL:,} | **Leverage:** {LEVERAGE}x | **Bias:** `{strategy['bias']}`")

# --- MASTER METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("SOL Live (API)", f"${current_price:,.2f}")
m2.metric("AI Auto-Range", f"${strategy['low']} - ${strategy['high']}")
# DANGER ZONE: Floor for Bullish, Ceiling for Bearish
m3.metric("Liquidation Risk", f"${strategy['liquidation']}", f"{strategy['safety_buffer']}% Buffer")
m4.metric("Market Sentiment", strategy['bias'])

# --- CHART ---
fig = go.Figure()

# Price Path
fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price", line=dict(color='#00ffa3', width=2)))

# Range Shading
x_area = df['ds'].tolist() + df['ds'].tolist()[::-1]
y_upper = [strategy['high']] * len(df)
y_lower = [strategy['low']] * len(df)
fig.add_trace(go.Scatter(x=x_area, y=y_upper + y_lower[::-1], fill='toself', 
                         fillcolor='rgba(0, 255, 163, 0.05)', line=dict(color='rgba(0,0,0,0)'), name="Target LP Range"))

# Risk Line
fig.add_trace(go.Scatter(x=df['ds'], y=[strategy['liquidation']] * len(df), 
                         name="LIQUIDATION DANGER", line=dict(color='#ff4b4b', width=3, dash='dot')))

fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=0, b=0),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

st.plotly_chart(fig, use_container_width=True)

# --- DANGER ALERTS ---
if strategy['bias'] == "BEARISH":
    st.error(f"⚠️ **Bearish Alert:** Risk is on the **HIGHER SIDE**. Liquidation ceiling at **${strategy['liquidation']}**.")
else:
    st.success(f"✅ **Bullish Alert:** Risk is on the **LOWER SIDE**. Liquidation floor at **${strategy['liquidation']}**.")

st.info(f"💡 **AI Strategy:** Deploy Concentrated Liquidity between **${strategy['low']}** and **${strategy['high']}**.")
