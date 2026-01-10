# Master Rule Book: Multi-source price fetching for SoldUSDC
from config import COINGECKO_BASE, DEXPAPRIKA_BASE, COINPAPRIKA_BASE
from utils.fallback import try_api

def get_soldusdc_price():
    """
    This tells the robot to check three different stores 
    to see how much SoldUSDC costs today.
    """
    # Master Rule: Use the specific Solana Contract Address for accuracy
    # (Note: Replace with actual SoldUSDC mint address if different)
    contract_address = "SoldUSDC_MINT_ADDRESS_HERE" 

    endpoints = [
        f"{COINGECKO_BASE}/simple/token_price/solana?contract_addresses={contract_address}&vs_currencies=usd",
        f"{DEXPAPRIKA_BASE}/networks/solana/tokens/{contract_address}",
        f"{COINPAPRIKA_BASE}/tickers/SoldUSDC"
    ]
    
    data = try_api(endpoints)
    
    if data:
        # We look inside the API answer for the price
        # Different stores give answers in different 'envelopes'
        try:
            if contract_address in data:
                return float(data[contract_address]["usd"])
            elif "price" in data:
                return float(data["price"])
            elif "quotes" in data:
                return float(data["quotes"]["USD"]["price"])
        except (KeyError, TypeError):
            return None
            
    return None
