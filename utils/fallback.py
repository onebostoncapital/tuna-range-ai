import time
import requests

def try_api(endpoints, params=None, timeout=5):
    for url in endpoints:
        try:
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"API failed: {url}, Error: {e}")
            continue
    return None
