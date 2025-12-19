from textblob import TextBlob
import pandas as pd


def analyze_news_sentiment(news_items):
    """
    Compute sentiment polarity for each news headline.
    """

    rows = []

    for item in news_items:
        text = item["title"]
        polarity = TextBlob(text).sentiment.polarity

        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        rows.append({
            "headline": text,
            "sentiment_score": round(polarity, 3),
            "sentiment": label
        })

    return pd.DataFrame(rows)

