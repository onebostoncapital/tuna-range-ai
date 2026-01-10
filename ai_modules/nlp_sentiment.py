# Master Rule Book: NLP Sentiment Engine
# This uses VADER to turn news headlines into a Risk Factor (0 to 1).
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_news_risk():
    """
    Reads market news and decides if the environment is scary.
    """
    # Later, we will connect this to real APIs like CryptoPanic.
    # For now, we use these sample headlines to test the logic.
    headlines = [
        "SoldUSDC liquidity is growing on DeFiTuna",
        "Market sentiment is steady",
        "Traders are cautious but optimistic"
    ]
    
    analyzer = SentimentIntensityAnalyzer()
    
    total_score = 0
    for text in headlines:
        # VADER gives a score from -1 (Bad) to 1 (Good)
        score = analyzer.polarity_scores(text)['compound']
        total_score += score

    # Calculate Average
    avg_sentiment = total_score / len(headlines)
    
    # Master Rule: Turn sentiment into a Risk Factor
    # 0.0 = Perfectly Safe (Happy news)
    # 1.0 = High Danger (Scary news)
    risk_factor = 1 - ((avg_sentiment + 1) / 2)
    
    return round(risk_factor, 2)
