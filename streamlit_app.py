# app.py
import streamlit as st
import altair as alt
import pandas as pd

# Read the .csv file

df = pd.read_csv("listings.csv")

# Display the first few rows of the dataframe
st.title("Displaying Pandas head() in Streamlit")

st.subheader("Using st.dataframe()")
st.dataframe(df.head())