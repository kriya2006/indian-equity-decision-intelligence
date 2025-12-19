import numpy as np


def estimate_news_impact(sentiment_df, price_df):
    """
    Estimate probable price impact based on sentiment intensity and volatility.
    """

    avg_sentiment = sentiment_df["sentiment_score"].mean()
    volatility = price_df["close"].pct_change().std()

    impact = avg_sentiment * volatility * 100

    return {
        "avg_sentiment": round(avg_sentiment, 3),
        "volatility": round(volatility * 100, 2),
        "impact_range": (
            round(impact - abs(impact), 2),
            round(impact + abs(impact), 2)
        )
    }
