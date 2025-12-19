import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol, period="1y"):
    """
    Fetch historical stock price data automatically.
    """

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    if df.empty:
        return None

    df = df.reset_index()
    df.rename(columns={"Close": "close"}, inplace=True)

    return df
