import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
st.set_page_config(
    page_title="Air BNB Analysis",
    layout="wide",
    initial_sidebar_state="expanded")
# CSS styling for the header and subheader
st.markdown(
    """
    <style>
    .header-container {
        background-color: red; /* Purple background */
        padding: 20px; /* Increased padding */
        border-radius: 15px; /* Rounded corners */
        width: 100%; /* Make the container broader */
        margin-left: 10px; /* Align to left margin */
        margin-bottom: 20px; /* Reduce gap between header and subheader */
    }
    .header-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        margin: 0; /* Remove default margin */
        font-size: 24px; /* Increase font size */
    }
    .subheader-container {
        background-color: purple; /* Purple background */
        padding: 5px; /* Padding around the text */
        border-radius: 10px; /* Rounded corners */
        width: 100%; /* Width of the container */
        margin-left: 10px; /* Align to left margin */
        margin-top: -10px; /* Reduce gap between header and subheader */
    }
    .subheader-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        font-size: 24px; /* Font size */
        margin: 0; /* Remove default margin */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Display the header with custom styling
st.markdown('<div class="header-container"><p class="header-text">Air  BNB  Analysis</p></div>', unsafe_allow_html=True)

# Display the subheader with custom styling
st.markdown('<div class="subheader-container"><p class="subheader-text">Travel Industry,Property Management and Tourism </p></div>', unsafe_allow_html=True)
df_air=pd.read_csv("output.csv")
print(df_air['cancellation_policy'].value_counts())
with st.container(height=700,border=True):
    st.image('C:/Users/ABI/Desktop/project4/airbnb.jpg',caption='Airbnb')
# Create a scatter plot
unique_df = df_air.groupby('country_name').agg({'latitude':'mean', 'longitude':'mean'}).reset_index()
fig = go.Figure()

for index, row in unique_df.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row['longitude']],
        lat=[row['latitude']],
        text=[row['country_name']],
        mode='markers',
        marker=dict(
            size=10,
            color='blue',  # You can change the color here
            opacity=0.8
        ),
        name=row['country_name']
    ))

fig.update_geos(
    projection_type="natural earth",
    showland=True, landcolor="rgb(243, 243, 243)",
    showocean=True, oceancolor="rgb(204, 230, 255)",
    showcountries=True
)

fig.update_layout(
    title='Country Locations',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth'
    )
)

# Display the map in Streamlit
st.plotly_chart(fig)
#st.image('C:/Users/ABI/Desktop/project4/images1.jpg',caption='Airbnb')
col1,col2=st.columns(2)
with col1:
    # Get the count of host names based on their location
    host_counts = df_air.groupby('country_name')['host_name'].count()

    # Plotting the horizontal bar plot
    fig, ax = plt.subplots()

    # Plotting horizontal bar chart
    host_counts.plot(kind='barh', ax=ax)

    # Customize the plot
    ax.set_xlabel('Count of Host Names')
    ax.set_ylabel('Host Location')
    ax.set_title('Horizontal Bar Plot of Host Names by Location')
    
    # Display the plot using Streamlit
    st.pyplot(fig)
    
with col2:
    # Calculate value counts of 'property_type'
    property_type_counts = df_air['property_type'].value_counts().head(10)

# Create a pie chart using Plotly Express
    fig = px.pie(property_type_counts, values=property_type_counts, names=property_type_counts.index, 
             title='Property Type Distribution')

# Display the plot using Streamlit
    st.plotly_chart(fig)

col3,col4=st.columns(2)
with col3:
   
   availability_counts = df_air['availability_365'].value_counts().reset_index()
   availability_counts.columns = ['availability', 'count']

# Sort values by availability
   availability_counts = availability_counts.sort_values(by='availability')

# Create Plotly line plot
   fig = px.line(availability_counts, x='availability', y='count', 
              labels={'availability': 'Availability', 'count': 'Count'},
              title='Availability Counts Line Plot')

# Display the plot in Streamlit
   st.plotly_chart(fig)
with col4:
    
    mean_prices_country = df_air.groupby('country_name')['price'].mean().reset_index()
    mean_prices_property_type=df_air.groupby('property_type')['price'].mean().reset_index()
    mean_prices_room_type=df_air.groupby('room_type')['price'].mean().reset_index()
    prices_option = st.selectbox('Prices At a Close Look:', ['country name', 'property type', 'room type'])
    if prices_option=='country name':
        fig = go.Figure(data=[go.Bar(x=mean_prices_country['country_name'], y=mean_prices_country['price'],marker_color='purple')])
        fig.update_layout(title='Mean Price by Country',
                  xaxis_title='Country',
                  yaxis_title='Mean Price in Dollars')
        st.plotly_chart(fig)
    elif prices_option=='property type':
        fig = go.Figure(data=[go.Bar(x=mean_prices_property_type['property_type'], y=mean_prices_property_type['price'],marker_color='yellow')])
        fig.update_layout(title='Mean Price by property type',
                  xaxis_title='property type',
                  yaxis_title='Mean Price in Dollars')
        st.plotly_chart(fig)
    elif prices_option=='room type':
        fig = go.Figure(data=[go.Bar(x=mean_prices_room_type['room_type'], y=mean_prices_room_type['price'],marker_color='grey')])
        fig.update_layout(title='Mean Price by room type',
                  xaxis_title='room type',
                  yaxis_title='Mean Price in Dollars')
        st.plotly_chart(fig)


with st.container():
    top_10_combinations = df_air[['property_type','accommodates']].value_counts().head(10).reset_index()
    top_10_combinations.columns = ['property_type', 'accommodates', 'count']

# Create the Altair chart
    chart = alt.Chart(top_10_combinations).mark_bar().encode(
    x='property_type',
    y='count',
    color='accommodates:N',
    tooltip=['property_type', 'accommodates', 'count']
).properties(
    title="Top 10 Property Types and Accommodations"
)

# Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

col5,col6=st.columns(2)
with col5:
    groupby_option = st.selectbox('Reviews:', ['country_name', 'property_type', 'room_type'])

# Show mean rating by selected category
    if groupby_option:
        st.subheader(f'Mean Rating by {groupby_option.capitalize()}')
        mean_rating_by_group = df_air.groupby(groupby_option)['review_scores_rating'].mean().reset_index()
        #st.write(mean_rating_by_group)
         # Define colors for bars
        custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # Plotting mean rating by selected category
        fig = px.bar(mean_rating_by_group, x=groupby_option, y='review_scores_rating', title=f'Mean Rating by {groupby_option.capitalize()}',color=groupby_option, color_discrete_sequence=custom_colors)
        st.plotly_chart(fig)
    
    
with col6:
    count_true_false = df_air['is_location_exact'].value_counts()

    #donut chart
    fig_donut = px.pie(names=count_true_false.index.astype(str), values=count_true_false.values, title='Count of exact location Info', hole=0.5)
    st.plotly_chart(fig_donut)

col7,col8=st.columns(2)
with col7:
    # Calculate count of each cancellation policy
    count_by_policy = df_air['cancellation_policy'].value_counts()

# Plotting count of each cancellation policy as a pie chart
    fig_pie = px.pie(names=count_by_policy.index, values=count_by_policy.values, title='Cancellation Policies')
    st.plotly_chart(fig_pie)
with col8:
    country_df = df_air.groupby('country_name', as_index=False)['bedrooms'].mean()
    country_df1=df_air.groupby('country_name', as_index=False)['cleaning_fee'].mean()
# Selectbox for hover text
    hover_text = st.selectbox('Select Hover Text', ['Mean Bedrooms','Mean Cleaning Fee'])

# Create scatter plot
    
# Update hover text based on selection
    if hover_text == 'Mean Bedrooms':
        fig = px.scatter_geo(
        data_frame=country_df,
        locations='country_name',
        locationmode='country names',
        lat=df_air.groupby('country_name')['latitude'].first(),
        lon=df_air.groupby('country_name')['longitude'].first(),
        size='bedrooms',
        color='bedrooms',
        hover_name='country_name',
        projection='natural earth',
        title='Average Number of Bedrooms by Country'
)

        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Mean Bedrooms: %{marker.size:.2f}<extra></extra>')
    
# Display the plot using Streamlit
        st.plotly_chart(fig)
    if hover_text == 'Mean Cleaning Fee':
        fig = px.scatter_geo(
        data_frame=country_df1,
        locations='country_name',
        locationmode='country names',
        lat=df_air.groupby('country_name')['latitude'].first(),
        lon=df_air.groupby('country_name')['longitude'].first(),
        size='cleaning_fee',
        color='cleaning_fee',
        hover_name='country_name',
        projection='natural earth',
        title='Average of cleaning fee by Country'
)

        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Mean cleaning fee: %{marker.size:.2f}<extra></extra>')
    
# Display the plot using Streamlit
        st.plotly_chart(fig)

