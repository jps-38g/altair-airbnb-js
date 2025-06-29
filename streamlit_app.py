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
df['review_scores_rating_bin'] = pd.cut(df['review_scores_rating'], bins=[0, 3, 3.5, 4, 4.5, 4.75, 4.99, 5],
                                    labels=['0 to 3','3 to 3.5', '3.5 to 4', '4 to 4.5', '4.5 to 4.75', '4.75 to 4.99', '5'])   
    

st.cache_data.clear()

#Convert the 'review_scores_rating_bin' column to a categorical type
df['review_scores_rating_bin'] = df['review_scores_rating_bin'].cat.add_categories('Missing').fillna('Missing')
df['review_scores_rating_bin'] = df['review_scores_rating_bin'].astype('category')

# Creating a list of rating bins for the selectbox using the unique values from the DataFrame
rating_bins = df['review_scores_rating_bin'].unique().tolist()

# Sorting the rating bins
rating_bins.sort()

st.title("Airbnb Available Listings By Neighborhood")

# Selectbox: Filter by Rating
# rating = st.selectbox("Filter by Property Rating", ["All"] + list(df["review_scores_rating_bin"].unique()))

rating = st.selectbox("Filter by Property Rating", ["All"] + rating_bins)

# Apply filters
filtered_props = df if rating == "All" else df[(df["review_scores_rating_bin"] == rating)]

# Create a bar chart with single selection
select_neighborhood = alt.selection_point(fields=['neighbourhood_cleansed'], on='click', empty='all')

# First chart: Bar chart of available properties by neighbourhood
bar_chart = alt.Chart(filtered_props).mark_bar().encode(
    x=alt.X('neighbourhood_cleansed').sort('-y'),
    y=alt.Y('count()', title='Available Property Count'),
    color=alt.condition(select_neighborhood, 'neighbourhood_cleansed', alt.value('lightgray'), legend=None),
    tooltip=['neighbourhood_cleansed', 'count()']
).add_params(      
    select_neighborhood
)

#st.altair_chart(bar_chart, use_container_width=False)

# Second chart: Bar Chart of Response Time By Hosts

bar_chart2 = alt.Chart(filtered_props, title="Bar Chart:  Property Counts By Host Response Time Bin").mark_bar().encode(
    y=alt.Y('host_response_time', title='Host Response Time').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="blues"))
).transform_filter(
    select_neighborhood
    )
    
#st.altair_chart(bar_chart2, use_container_width=False)

# Third chart: Bar Chart of Properties By Binned Number of Days Available
bar_chart3 = alt.Chart(filtered_props, title="Bar Chart: Property Counts By # of Days Available In Last Year").mark_bar().encode(
    y=alt.Y('availability_365_bin', title='# of Days Available in Last Year').sort('-x'),
    x=alt.Y('count()', title='Property Count'),
    color=alt.Color("count()", scale=alt.Scale(scheme="blues"))
 ).transform_filter(
    select_neighborhood
    )

#st.altair_chart(bar_chart3, use_container_width=False)

# Combine and display the charts

bottom_charts = bar_chart2 | bar_chart3

st.altair_chart(alt.vconcat(bar_chart, bottom_charts),use_container_width=False)
