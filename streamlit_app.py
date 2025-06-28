# app.py
import streamlit as st
import altair as alt
import pandas as pd

# Read the .csv file
df = pd.read_csv("listings.csv")


st.set_page_config(page_title="Interactive Dashboard", layout="wide")

# Display the first few rows of the dataframe
#st.title("Displaying Pandas head() in Streamlit")

#st.subheader("Using st.dataframe()")
#st.dataframe(df.head())

bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('neighbourhood_cleansed').sort('-y'),
    y=alt.Y('count()', title='Available Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
    )

st.altair_chart(bar_chart, use_container_width=False)