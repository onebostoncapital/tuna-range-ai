# Master Rule Book: News & Sentiment Intelligence (CryptoPanic, RSS, VADER)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NewsAnalyzer:
    """
    This is how the robot listens to news. 
    It reads headlines and gives a 'Risk Factor' score.
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment_risk(self, news_headlines=None):
        # If we don't have news yet, we use a neutral starting point
        if not news_headlines:
            news_headlines = [
                "Market is steady for SoldUSDC",
                "New liquidity added to DeFiTuna"
            ]

        total_score = 0
        for text in news_headlines:
            # The robot reads each headline and gives it a score from -1 to 1
            score = self.analyzer.polarity_scores(text)
            total_score += score['compound']

        # We calculate the average sentiment
        avg_sentiment = total_score / len(news_headlines)
        
        # Master Rule: Generate a 'News Risk Factor'
        # 1.0 is very risky (scary news), 0.0 is very safe (happy news)
        risk_factor = 1 - ((avg_sentiment + 1) / 2)
        
        return {
            "sentiment_score": round(avg_sentiment, 2),
            "risk_factor": round(risk_factor, 2),
            "summary": "Positive" if avg_sentiment > 0.05 else "Negative" if avg_sentiment < -0.05 else "Neutral"
        }
