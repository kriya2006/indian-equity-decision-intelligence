import streamlit as st
import pandas as pd
from models.ml_longterm_ranker import compute_decision_quality

st.set_page_config(page_title="Indian Equity Decision Intelligence", layout="wide")

st.title("📊 Indian Equity Decision Quality Engine")
st.caption("Evaluating investment decisions — not predicting prices.")

df = pd.read_csv("data/indian_equities.csv", parse_dates=["date"])

processed = compute_decision_quality(df)

st.subheader("Decision Quality Breakdown")

quality_counts = processed["decision_quality"].value_counts()
st.bar_chart(quality_counts)

st.subheader("Annotated Trade-Level Data")
st.dataframe(processed)
