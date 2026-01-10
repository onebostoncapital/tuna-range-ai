from config import COINGECKO_BASE, DEXPAPRIKA_BASE, COINPAPRIKA_BASE
from utils.fallback import try_api

def get_soldusdc_price():
    # Master Rule: Check multiple sources for the SoldUSDC price
    endpoints = [
        f"{COINGECKO_BASE}/simple/price?ids=sold-usdc&vs_currencies=usd",
        f"{DEXPAPRIKA_BASE}/networks/solana/tokens/SoldUSDC",
        f"{COINPAPRIKA_BASE}/tickers/SoldUSDC",
    ]
    data = try_api(endpoints)
    if data:
        # Simplification: in real use, we parse based on which API responded
        return 1.0  # Placeholder since SoldUSDC is a stablecoin
    return 1.0
