import pandas as pd
import numpy as np

def detect_market_context(df):
    df = df.sort_values(["symbol", "date"])

    # Rolling features
    df["return"] = df.groupby("symbol")["close"].pct_change()
    df["volatility"] = df.groupby("symbol")["return"].rolling(20).std().reset_index(0, drop=True)
    df["trend_short"] = df.groupby("symbol")["close"].rolling(50).mean().reset_index(0, drop=True)
    df["trend_long"] = df.groupby("symbol")["close"].rolling(200).mean().reset_index(0, drop=True)

    def classify(row):
        if pd.isna(row["trend_long"]) or pd.isna(row["volatility"]):
            return "Insufficient Data"

        if row["trend_short"] > row["trend_long"] and row["volatility"] < 0.02:
            return "Trending (Investor Friendly)"
        elif row["volatility"] >= 0.04:
            return "High-Risk Volatile"
        else:
            return "Sideways / Noisy"

    df["market_context"] = df.apply(classify, axis=1)

    return df
