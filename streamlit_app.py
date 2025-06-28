# app.py
import streamlit as st
import altair as alt
import pandas as pd

# Read the .csv file
df = pd.read_csv("listings.csv")

# Create a New Character Column Describing Bin Ranges of Days Available
df['availability_365_bin'] = pd.cut(df['availability_365'], bins=[50, 100, 150, 200, 250, 300, 365],
                                    labels=['50-100', '100-150', '150-200', '200-250', '250-300', '300-365'])   

# Display the first few rows of the dataframe
#st.title("Displaying Pandas head() in Streamlit")

#st.subheader("Using st.dataframe()")
#st.dataframe(df.head())

# First chart: Bar chart of available properties by neighbourhood
st.title("Airbnb Available Listings")
bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('neighbourhood_cleansed').sort('-y'),
    y=alt.Y('count()', title='Available Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
    )

st.altair_chart(bar_chart, use_container_width=False)

# Second chart: Bar Chart of Response Time By Hosts

bar_chart2 = alt.Chart(df, title="Bar Chart:  Property Counts By Host Response Time Bin").mark_bar().encode(
    y=alt.Y('host_response_time', title='Host Response Time').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
)
st.altair_chart(bar_chart2, use_container_width=False)

# Third chart: Bar Chart of Properties By Binned Number of Days Available
bar_chart3 = alt.Chart(df, title="Bar Chart: Property Counts By Number of Days Available").mark_bar().encode(
    y=alt.Y('availability_365_bin', title='Number of Days Available').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
)
st.altair_chart(bar_chart3, use_container_width=False)