import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor
from ai_modules.nlp_sentiment import get_news_risk

# --- PAGE CONFIG ---
st.set_page_config(page_title="DeFiTuna AI", page_icon="🐟", layout="wide")
st.title("🐟 DeFiTuna: SoldUSDC AI Decision Engine")

# --- DATA LOADING ---
with st.sidebar:
    st.header("System Status")
    df = get_live_market_data()
    if df is not None:
        st.success("Connected to CoinGecko")
    else:
        st.error("Data Source Offline")

if df is not None:
    # 1. BRAIN CALCULATIONS
    price = get_soldusdc_price()
    indicators = compute_technical_indicators(df)
    news_risk = get_news_risk() # Note: Uses your placeholder logic
    
    if indicators:
        floor = calculate_floor(price, indicators, news_risk)
        
        # 2. TOP LEVEL METRICS
        m1, m2, m3 = st.columns(3)
        m1.metric("SOL Price (Market Trend)", f"${price:,.2f}")
        m2.metric("Calculated Safety Floor", f"${floor:,.2f}")
        m3.metric("Volatility (ATR)", f"{round(indicators['ATR'], 4)}")

        # 3. STRATEGY BOX
        st.divider()
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Market Trend Analysis")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price", line=dict(color='#00FFA3')))
            fig.add_trace(go.Scatter(x=df['ds'], y=[floor]*len(df), name="Liquidity Floor", line=dict(color='red', dash='dash')))
            fig.update_layout(template="plotly_dark", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("AI Recommendation")
            if price < floor:
                st.error("🚨 DO NOT PROVIDE LP\nPrice is below structural safety floor.")
            elif news_risk > 0.6:
                st.warning("⚠️ PROCEED WITH CAUTION\nHigh news risk detected.")
            else:
                st.success("✅ OPTIMAL CONDITIONS\nMarket is trend-healthy for LP.")
                st.info(f"Suggested Range: ${round(floor, 2)} — ${round(price * 1.1, 2)}")
    else:
        st.info("Gathering enough historical data to calculate indicators... Wait 5 seconds.")
else:
    st.warning("🔄 Attempting to bypass Yahoo rate limits... System is switching to CoinGecko API.")
