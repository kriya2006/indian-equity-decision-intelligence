import feedparser
from urllib.parse import quote


def fetch_stock_news(stock_name, max_items=8):
    """
    Fetch latest news headlines for a stock using Google News RSS.
    """

    query = f"{stock_name} stock"
    encoded_query = quote(query)

    url = (
        f"https://news.google.com/rss/search?"
        f"q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    news_items = []

    for entry in feed.entries[:max_items]:
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, "published", ""),
            "source": getattr(entry.source, "title", "Google News")
        })

    return news_items
