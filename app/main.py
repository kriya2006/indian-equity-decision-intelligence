import sys
from pathlib import Path

# -----------------------
# PATH SETUP
# -----------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# -----------------------
# IMPORTS
# -----------------------
import streamlit as st
import pandas as pd

from utils.stock_data import fetch_stock_data
from utils.news_fetcher import fetch_stock_news
from utils.market_context import detect_market_context
from utils.behavioral_bias import detect_behavioral_bias
from utils.news_sentiment import analyze_news_sentiment
from utils.news_impact import estimate_news_impact
from models.ml_longterm_ranker import compute_decision_quality

# -----------------------
# APP HEADER
# -----------------------
st.title("Indian Equity Decision Intelligence Engine")
st.caption(
    "A unified stock intelligence prototype combining price, news, sentiment, "
    "market context, and behavioral decision analytics."
)

# -----------------------
# STOCK SELECTOR
# -----------------------
st.subheader("🔍 Stock Selector")

stock_list = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "TATAELXSI.NS",
    "COFORGE.NS",
    "PIIND.NS",
    "IRFC.NS",
    "SJVN.NS",
    "YESBANK.NS"
]

symbol = st.selectbox("Select Stock", stock_list)

custom_symbol = st.text_input(
    "Or enter any NSE stock symbol manually (e.g. ABC.NS)",
    value=""
)

if custom_symbol:
    symbol = custom_symbol.upper()

period = st.selectbox(
    "Select time range",
    ["1mo", "3mo", "6mo", "1y", "2y"],
    index=3
)

analyze = st.button("🔎 Analyze Stock")

if not analyze:
    st.info("Select a stock and click **Analyze Stock** to begin.")
    st.stop()

# -----------------------
# FETCH STOCK DATA
# -----------------------
df = fetch_stock_data(symbol, period)

if df is None or df.empty:
    st.error("Unable to fetch stock data. Try another symbol.")
    st.stop()

df["symbol"] = symbol
df.rename(columns={"Date": "date"}, inplace=True)

# -----------------------
# LIVE PRICE & CHART
# -----------------------
st.subheader("📈 Live Price Overview")

cmp = round(df["close"].iloc[-1], 2)
st.metric("Current Market Price (CMP)", f"₹ {cmp}")

st.line_chart(df.set_index("date")["close"])

# -----------------------
# NEWS AGGREGATION
# -----------------------
st.subheader("📰 Latest News")

stock_name = symbol.split(".")[0]
news = fetch_stock_news(stock_name)

if not news:
    st.write("No recent news found.")
else:
    for item in news:
        st.markdown(f"**{item['title']}**")
        st.caption(f"{item['source']} | {item['published']}")
        st.markdown(f"[Read more]({item['link']})")
        st.markdown("---")

# -----------------------
# NEWS SENTIMENT
# -----------------------
st.subheader("🧠 News Sentiment Analysis")

sentiment_df = analyze_news_sentiment(news)
st.dataframe(sentiment_df)

avg_sentiment = sentiment_df["sentiment_score"].mean()
st.metric("Overall News Sentiment", round(avg_sentiment, 3))

# -----------------------
# MARKET IMPACT
# -----------------------
st.subheader("📉 Estimated Market Impact")

impact = estimate_news_impact(sentiment_df, df)

st.write(f"""
**What this means:**
- Average sentiment score: **{impact['avg_sentiment']}**
- Recent volatility: **{impact['volatility']}%**
- Expected short-term impact range:  
  **{impact['impact_range'][0]}% to {impact['impact_range'][1]}%**
""")

st.caption(
    "Impact is statistically estimated from sentiment intensity and recent volatility. "
    "This is not a price prediction."
)

# -----------------------
# MARKET CONTEXT
# -----------------------
st.subheader("🌍 Market Context Engine")

context_df = detect_market_context(df)

latest_context = (
    context_df.sort_values("date")
    .groupby("symbol")
    .tail(1)[["symbol", "market_context", "volatility"]]
)

st.dataframe(latest_context)

# -----------------------
# DECISION QUALITY
# -----------------------
st.subheader("🧠 Decision Quality Analysis")

processed = compute_decision_quality(context_df)

st.bar_chart(processed["decision_quality"].value_counts())

st.dataframe(
    processed[["symbol", "date", "return_%", "decision_quality"]].head(20)
)

# -----------------------
# BEHAVIORAL BIAS
# -----------------------
st.subheader("⚠️ Behavioral Bias Diagnostics")

processed = detect_behavioral_bias(processed)

st.dataframe(
    processed[
        ["symbol", "date", "return_%", "decision_quality", "behavioral_bias"]
    ].head(20)
)

# -----------------------
# DECISION QUALITY SCORE
# -----------------------
st.subheader("📊 Decision Quality Score (DQS)")

def compute_dqs(row):
    if row["decision_quality"] == "High Quality Decision":
        return 85
    elif row["decision_quality"] == "Neutral Decision":
        return 55
    elif row["decision_quality"] == "Poor Decision":
        return 25
    else:
        return 0

processed["DQS"] = processed.apply(compute_dqs, axis=1)
avg_dqs = int(processed["DQS"].mean())

st.metric("Average DQS", avg_dqs)

# -----------------------
# DATA-DRIVEN INSIGHTS
# -----------------------
st.subheader("📝 Data-Driven Insights")

bad_decisions = processed[processed["DQS"] < 40].shape[0]
good_decisions = processed[processed["DQS"] > 70].shape[0]

st.write(
    f"""
    • {good_decisions} decisions aligned well with market context  
    • {bad_decisions} decisions show emotional or timing bias  
    • Risky environments amplify behavioral mistakes
    """
)

# -----------------------
# HOLDING PERIOD SUITABILITY
# -----------------------
st.subheader("⏳ Holding Period Suitability Analysis")

volatility = impact["volatility"]

st.markdown("### 🔴 Intraday Trader Perspective")
if volatility < 2:
    st.write(
        "Low volatility and weak catalysts suggest limited intraday opportunity. "
        "Emotional entries in such conditions historically reduce decision quality."
    )
else:
    st.write(
        "Higher volatility enables short-term movement, but requires strict discipline "
        "to avoid emotionally driven trades."
    )

st.markdown("### 🟡 Mid-Term Trader Perspective (Weeks to Months)")
if 40 <= avg_dqs <= 60:
    st.write(
        "Mixed decision quality indicates timing sensitivity. Gradual entries "
        "and avoidance of news overreaction are critical."
    )
else:
    st.write(
        "Either strong conviction or elevated uncertainty detected. "
        "Risk management becomes essential."
    )

st.markdown("### 🟢 Long-Term Investor Perspective")
if avg_sentiment >= 0 and volatility < 3:
    st.write(
        "Stable sentiment and controlled volatility favor long-term, process-driven investing. "
        "Historical data supports patience over reaction."
    )
else:
    st.write(
        "Long-term investors should monitor shifts in sentiment and volatility closely."
    )

st.caption(
    "This system does not give buy/sell recommendations. "
    "It frames decision suitability using data, behavior, and risk."
)

# -----------------------
# CONTEXT VS DECISION
# -----------------------
st.subheader("🔗 Market Context vs Decision Quality")

context_quality = (
    processed.groupby(["market_context", "decision_quality"])
    .size()
    .unstack(fill_value=0)
)

st.dataframe(context_quality)
