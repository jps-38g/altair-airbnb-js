# app.py
import streamlit as st
import altair as alt
import pandas as pd

# Read the .csv file
df = pd.read_csv("listings.csv")

# Create a New Character Column Describing Bin Ranges of Days Available
df['availability_365_bin'] = pd.cut(df['availability_365'], bins=[0, 50, 100, 150, 200, 250, 300, 365],
                                    labels=['0-50','50-100', '100-150', '150-200', '200-250', '250-300', '300-365'])   


# Create a New Character Column Describing Bin Ranges of Review Score Ratings
df['review_scores_rating_bin'] = pd.cut(df['review_scores_rating'], bins=[0, 3, 3.5, 4, 4.5, 4.75, 5],
                                    labels=['0 to 3','3 to 3.5', '3.5 to 4', '4 to 4.5', '4.5 to 4.75', '4.75 to 5'])   
    

st.cache_data.clear()

# Selectbox: Filter by Rating
rating = st.selectbox("Filter by Property Rating", ["All"] + list(df["review_scores_rating_bin"].unique()))

# Apply filters
filtered_props = df if rating == "All" else df[(df["review_scores_rating_bin"] == rating)]

# First chart: Bar chart of available properties by neighbourhood
st.title("Airbnb Available Listings")
bar_chart = alt.Chart(filtered_props).mark_bar().encode(
    x=alt.X('neighbourhood_cleansed').sort('-y'),
    y=alt.Y('count()', title='Available Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
    )

st.altair_chart(bar_chart, use_container_width=False)

# Second chart: Bar Chart of Response Time By Hosts

bar_chart2 = alt.Chart(filtered_props, title="Bar Chart:  Property Counts By Host Response Time Bin").mark_bar().encode(
    y=alt.Y('host_response_time', title='Host Response Time').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
)
st.altair_chart(bar_chart2, use_container_width=False)

# Third chart: Bar Chart of Properties By Binned Number of Days Available
bar_chart3 = alt.Chart(filtered_props, title="Bar Chart: Property Counts By Number of Days Available").mark_bar().encode(
    y=alt.Y('availability_365_bin', title='Number of Days Available').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="greens"))
)
st.altair_chart(bar_chart3, use_container_width=False)