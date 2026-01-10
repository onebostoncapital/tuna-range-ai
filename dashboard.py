# Master Rule Book: Streamlit Dashboard
# This is the face of our AI-powered decision engine.
import streamlit as st
import pandas as pd
import numpy as np
import config
from apis.price_data import get_soldusdc_price
from calculations.indicators import compute_technical_indicators
from calculations.liquidity_floor import calculate_floor
from ai_modules.nlp_sentiment import get_news_risk

# --- Page Setup ---
st.set_page_config(page_title="TunaRange AI", layout="wide")
st.title("🐟 SoldUSDC Decision Engine")
st.write(f"Analyzing liquidity exclusively for **DeFiTuna**")

# --- 1. Data Collection ---
# Get current price and news risk
price = get_soldusdc_price()
news_risk = get_news_risk()

# Create dummy data for math demonstration (MA20/MA200)
# In the next version, we will pull real history from APIs.
data = {
    'close': np.random.normal(1.0, 0.005, 300).cumsum() + 10,
    'high': np.random.normal(1.005, 0.005, 300).cumsum() + 10,
    'low': np.random.normal(0.995, 0.005, 300).cumsum() + 10,
}
df = pd.DataFrame(data)

# --- 2. Brain Work ---
indicators = compute_technical_indicators(df)
floor = calculate_floor(price, indicators, news_risk)

# --- 3. Display Results ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("SoldUSDC Price", f"${price}")
    st.write(f"Source: Multi-API Fallback")

with col2:
    st.metric("Liquidity Floor", f"${floor}")
    st.write("Safety Shield: Active")

with col3:
    risk_level = "Safe" if news_risk < 0.4 else "Moderate" if news_risk < 0.7 else "High"
    st.metric("News Risk Factor", f"{news_risk}", delta=risk_level, delta_color="inverse")

st.divider()

# Final Recommendation as per Master Rule Book
st.header("🎯 Final LP Strategy")
if news_risk > 0.75:
    st.error("ACTION: **WAIT** (Risk too high for safe liquidity)")
elif price < floor:
    st.warning("ACTION: **ADJUST RANGE** (Price below safety floor)")
else:
    st.success("ACTION: **LP PROVIDE** (Conditions optimal for DeFiTuna)")

# Show some math for the curious
with st.expander("See Technical Indicators"):
    st.write(indicators)
