"""Simple test version of the Streamlit app"""

import streamlit as st
import pandas as pd

st.title("✈️ Flight Delay Analysis - TEST")
st.write("Testing if app loads...")

# Try to load data
try:
    data = pd.read_csv('flights.csv')
    st.success(f"✅ Data loaded! {len(data)} rows")
    st.dataframe(data.head(5))
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
