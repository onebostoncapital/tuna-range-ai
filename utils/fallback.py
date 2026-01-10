# Master Rule Book: API Fallback Logic with Retry/Timeout
import time
import requests

def try_api(endpoints, params=None, timeout=5):
    """
    If the first API is broken, try the second. 
    If that fails, try the third.
    """
    for url in endpoints:
        # We try 3 times for each URL before moving to the next one
        for attempt in range(3): 
            try:
                response = requests.get(url, params=params, timeout=timeout)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429: # Too many requests
                    time.sleep(2) # Wait 2 seconds and try again
            except Exception as e:
                print(f"Connection failed for {url}: {e}")
        
    print("CRITICAL: All API sources failed!")
    return None
