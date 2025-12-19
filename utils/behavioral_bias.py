import pandas as pd
import numpy as np

def detect_behavioral_bias(df):
    """
    Detects common investor biases from historical decisions.
    """

    bias_flags = []

    for _, row in df.iterrows():
        if row["return_%"] < -5:
            bias_flags.append("Loss Aversion / Bad Hold")
        elif row["return_%"] > 10:
            bias_flags.append("Good Conviction")
        else:
            bias_flags.append("Normal Decision")

    df["behavioral_bias"] = bias_flags
    return df
