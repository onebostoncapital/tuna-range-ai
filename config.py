# Master Rule Book: Centralized API Keys and LP Parameters
# Do not share this file if it contains real keys!

# --- API Endpoints ---
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
DEXPAPRIKA_BASE = "https://api.dexpaprika.com"
COINPAPRIKA_BASE = "https://api.coinpaprika.com/v1"

# --- Tickers & Pairs ---
YAHOO_TICKER = "SoldUSDC-USD"
PAIR_NAME = "SoldUSDC"

# --- Security & Keys ---
# TIP: In a real project, we use 'Environment Variables' for these
CRYPTOPANIC_KEY = "YOUR_CRYPTO_PANIC_API_KEY"
GOOGLE_NEWS_API_KEY = "YOUR_GOOGLE_NEWS_API_KEY"

# --- LP Strategy Parameters ---
# These control how wide or narrow our safety ranges are
ATR_MULTIPLIER = 1.5
LP_RANGE_MULTIPLIER = 1.2
RISK_FREE_RATE = 0.05  # 5% baseline for calculations
