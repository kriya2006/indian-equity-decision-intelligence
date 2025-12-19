import pandas as pd
import numpy as np

def compute_decision_quality(df, lookahead_days=5):
    """
    Measures whether a BUY decision was good *given future outcomes*
    without pretending we can predict the future.
    """

    df = df.sort_values(["symbol", "date"])
    df["future_close"] = df.groupby("symbol")["close"].shift(-lookahead_days)

    df["return_%"] = (df["future_close"] - df["close"]) / df["close"] * 100

    conditions = [
        df["return_%"] > 5,
        (df["return_%"] >= -2) & (df["return_%"] <= 5),
        df["return_%"] < -2
    ]

    labels = ["High Quality Decision", "Neutral Decision", "Poor Decision"]

    df["decision_quality"] = np.select(conditions, labels, default="Unknown")

    return df
