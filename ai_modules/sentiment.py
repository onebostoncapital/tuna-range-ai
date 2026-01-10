# Master Rule Book: Aggregated News Risk Factor from Multi-Sources
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NewsAnalyzer:
    """
    The robot now has three ears: 
    1. CryptoPanic (Live market pulses)
    2. CoinDesk/RSS (Professional news)
    3. Google News (General world trends)
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        # In a real setup, you'd put your API keys here
        self.sources = ["CryptoPanic", "CoinDesk", "GoogleNews"]

    def fetch_cryptopanic(self):
        # This is a placeholder for the real API call
        # It usually returns things like: 'BTC is breaking out!'
        return ["SoldUSDC volume is spiking on DeFiTuna", "Solana ecosystem sees major growth"]

    def fetch_rss_feeds(self):
        # This simulates reading from CoinDesk or CoinTelegraph RSS
        return ["New stablecoin regulations proposed", "DeFi usage hits all-time high"]

    def get_sentiment_risk(self):
        # Master Rule: Combine all sources
        all_headlines = self.fetch_cryptopanic() + self.fetch_rss_feeds()
        
        total_score = 0
        for text in all_headlines:
            score = self.analyzer.polarity_scores(text)['compound']
            total_score += score

        avg_sentiment = total_score / len(all_headlines)
        
        # Master Rule: Calculate the News Risk Factor (0.0 safe, 1.0 risky)
        # We also look for 'Scary Words' to increase risk automatically
        scary_words = ["hack", "exploit", "crash", "ban", "scam"]
        danger_boost = 0
        for text in all_headlines:
            if any(word in text.lower() for word in scary_words):
                danger_boost += 0.2

        risk_factor = max(0, min(1, (1 - ((avg_sentiment + 1) / 2)) + danger_boost))
        
        return {
            "risk_factor": round(risk_factor, 2),
            "sentiment": "Bullish" if avg_sentiment > 0.1 else "Bearish" if avg_sentiment < -0.1 else "Neutral",
            "sources_checked": len(self.sources)
        }
