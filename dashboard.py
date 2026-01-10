import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor
from ai_modules.nlp_sentiment import get_news_risk

st.set_page_config(page_title="SoldUSDC AI Dashboard", layout="wide")
st.title("🛡️ SoldUSDC AI Risk Engine")

# --- DATA RELOAD ---
df = get_live_market_data()

if df is not None and not df.empty:
    price = get_soldusdc_price()
    indicators = compute_technical_indicators(df)
    news_risk = get_news_risk()
    
    if indicators:
        floor = calculate_floor(price, indicators, news_risk)
        
        # 1. Metrics Header
        c1, c2, c3 = st.columns(3)
        c1.metric("SOL Price (Proxy)", f"${price}")
        c2.metric("Safety Floor", f"${floor}")
        c3.metric("News Risk Score", f"{int(news_risk*100)}%")
        
        # 2. Strategy Recommendation
        st.subheader("Final AI Decision")
        if news_risk > 0.6:
            st.error("🚨 HIGH RISK: News sentiment is crashing. Stay in USDC.")
        elif price < floor:
            st.warning("⚠️ FLOOR BREACH: Price is below safety floor. Adjust LP range.")
        else:
            st.success("✅ OPTIMAL: Provide Liquidity. High probability of range-bound behavior.")

        # 3. Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price (SOL)"))
        fig.add_trace(go.Scatter(x=df['ds'], y=[floor]*len(df), name="Risk Floor", line=dict(color='red', dash='dash')))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Calculating indicators... Not enough history yet.")
else:
    st.error("Connecting to Market Data... If this persists, Yahoo is rate-limiting the IP.")
