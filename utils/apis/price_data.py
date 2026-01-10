# Master Rule Book: Price & Technical Data with Fallback Logic
import config
from utils.fallback import try_api

class PriceAggregator:
    def get_latest_price(self):
        # List of endpoints from our Master Rule Book
        endpoints = [
            f"{config.COINGECKO_BASE}/simple/price?ids=solana&vs_currencies=usd",
            f"{config.COINPAPRIKA_BASE}/tickers/sol-solana"
        ]
        
        data = try_api(endpoints)
        # Logic to extract the price based on which API answered...
        return data
