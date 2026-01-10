# Master Rule Book: Live AI Dashboard
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from apis.price_data import get_live_market_data, get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor
from ai_modules.nlp_sentiment import get_news_risk
from ai_modules.ml_forecast import PriceForecaster

# --- Setup ---
st.set_page_config(page_title="SoldUSDC AI Engine", layout="wide")
st.title("🤖 SoldUSDC Live Decision Engine")

# --- 1. Get REAL Data ---
with st.spinner('Connecting to Solana Market Data...'):
    df = get_live_market_data()
    price = get_soldusdc_price()
    news_risk = get_news_risk()

if df is not None:
    # --- 2. Run AI Brains ---
    indicators = compute_technical_indicators(df)
    forecaster = PriceForecaster()
    prediction = forecaster.predict(df)
    floor = calculate_floor(price, indicators, news_risk)

    # --- 3. Top Row Metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Live Price", f"${price}")
    m2.metric("Safety Floor", f"${floor}")
    m3.metric("AI Bias", prediction['directional_bias'])
    m4.metric("News Risk", f"{int(news_risk * 100)}%")

    # --- 4. Real Price Chart ---
    st.subheader("Market Analysis & Safety Floor")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Price", line=dict(color='gold')))
    fig.add_trace(go.Scatter(x=df['ds'], y=[floor]*len(df), name="Liquidity Floor", line=dict(dash='dash', color='red')))
    st.plotly_chart(fig, use_container_width=True)

    # --- 5. Final Recommendation ---
    st.divider()
    if news_risk > 0.6:
        st.error(f"🛑 STRATEGY: WAIT. News risk ({news_risk}) is too high for safe LP.")
    elif price < floor:
        st.warning("⚠️ STRATEGY: ADJUST. Price is touching the safety floor.")
    else:
        st.success(f"✅ STRATEGY: PROVIDE LP. Target Range: ${floor} - ${round(price * 1.05, 4)}")
else:
    st.error("Could not connect to live data. Please check your internet or API limits.")
