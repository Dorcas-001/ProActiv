import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
teal_color = '#009DAE'  # Teal green color code
green_EC = '#138024'
tangerine_color = '#E66C37'  # Tangerine orange color code
st.markdown(
    """
    <style>
    .main-title{
        color: #e66c37
        text_align: center;
        font_size: 3rem;
        font_wight: bold;
        margin_bottom=.5rem;
        text_shadow: 1px 1px 2px rgba(0,0,0.1);
    }
    .reportview-container {
        background-color: #013220;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #013220;
        color: white;
    }
    .metric .metric-value {
        color: #008040;
    }
    .metric .mertic-title {
        color: #FFA500;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('''
    <style>
        .main-title {
            color: #E66C37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)
# Your Streamlit app content
st.markdown('<h1 class = "main-title">Step Count Dashboard</h1>', unsafe_allow_html=True)
# Loading the data
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']


df = pd.read_excel("steps_data.xlsx")

# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h2 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)


# Ensure the 'Start Date' column is in datetime format if needed

# Sidebar for filters
st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=sorted(df['Year'].dropna().unique()))

# Filtered DataFrame
filtered_df = df

# Apply filters to the DataFrame
if year:
    filtered_df = filtered_df[filtered_df['Year'].isin(year)]


# Determine the filter description
filter_description = ""
if year:
    filter_description += f"{', '.join(map(str, year))} "


if not filter_description:
    filter_description = "All df"



if not filtered_df.empty:
     # Calculate metrics
    scaling_factor = 1_000_000
    # Filter for the years 2023 and 2024
    df_2023 = filtered_df[filtered_df['Year'] == 2023]
    df_2024 = filtered_df[filtered_df['Year'] == 2024]
    # Calculate total steps for each year
    total_steps_2023 = df_2023['steps'].sum()
    total_steps_2024 = df_2024['steps'].sum()
    distance = filtered_df["distance"].sum()
    total_steps_per_member = filtered_df.groupby('member_account_id')['steps'].sum()
    average_steps_per_member = total_steps_per_member.mean()
    # Count unique members
    unique_members = filtered_df['member_account_id'].nunique()

    scaled_steps_2024 = total_steps_2024/scaling_factor
    scaled_distance = distance/scaling_factor


    # Create 4-column layout for metric cards
    col1, col2, col3, col4, col5 = st.columns(5)

    # Define CSS for the styled boxes
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
        }
        .metric-title {
            color: #e66c37; /* Change this color to your preferred title color */
            font-size: 1em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1.5em;
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
        

    display_metric(col1, "Total Step Count 2023", total_steps_2023)
    display_metric(col2, "Total Step Count 2024", f"{scaled_steps_2024:.0f}M")
    display_metric(col3, "Total Unique Members", unique_members)
    display_metric(col4, "Total Distance Covered", f"{scaled_distance:.0f}M")
    display_metric(col5, "Average steps per Member", f"{average_steps_per_member:.1f}")




   
    # Sidebar styling and logo
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #007BFF; /* Change this color to your preferred title color */
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-title {
            color: #e66c37;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-header {
            color: #e66c37; /* Change this color to your preferred header color */
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-multiselect {
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content .logo img {
            max-width: 80%;
            height: auto;
            border-radius: 50%;
        }
                
        </style>
        """, unsafe_allow_html=True)
    

    # Group by year and calculate the average steps
    yearly_avg_steps_august = filtered_df.groupby('Year')['steps'].mean().reset_index()

    # Format the average steps to 2 decimal places
    yearly_avg_steps_august['formatted_steps'] = yearly_avg_steps_august['steps'].apply(lambda x: f"{x:.2f}")

    # Define custom colors
    custom_colors = ["#006E7F", "#e66c37", "#B4B4B8"]

    # Streamlit layout
    cols1, cols2 = st.columns(2)

    with cols1:
        # Create the bar chart
        fig_yearly_avg_steps_august = go.Figure()

        fig_yearly_avg_steps_august.add_trace(go.Bar(
            x=yearly_avg_steps_august['Year'],
            y=yearly_avg_steps_august['steps'],
            text=yearly_avg_steps_august['formatted_steps'],
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y',
            marker_color=custom_colors[0]  # Use the first custom color
        ))

        fig_yearly_avg_steps_august.update_layout(
            xaxis_title="Year",
            yaxis_title="Average Steps",
            font=dict(color='Black'),
            xaxis=dict(
                title_font=dict(size=14), 
                tickfont=dict(size=12),
                tickmode='array',
                tickvals=yearly_avg_steps_august['Year'].tolist(),  # Set tick values based on unique years in the data
                ticktext=yearly_avg_steps_august['Year'].astype(str).tolist()  # Set tick labels as strings of the years
            ),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
            height=450
        )

        # Display the chart in Streamlit
        st.markdown('<h2 class="custom-subheader">Yearly Average Steps in August</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_yearly_avg_steps_august, use_container_width=True)


        # Sum the steps for each hour
    hourly_steps = filtered_df.groupby('HourOfDay')['steps'].mean().sort_index()
    with cols2:
        # Create the bar chart
        fig = go.Figure()

        # Add bar trace
        fig.add_trace(go.Bar(
            x=hourly_steps.index,
            y=hourly_steps.values,
            name='Number of Steps',
            marker_color=['#009DAE' if hour in range(6, 18) else '#e66c37' for hour in hourly_steps.index]
        ))

        # Update layout
        fig.update_layout(
            xaxis_title='Hour of the Day',
            yaxis_title='Average Number of Steps',
            legend_title='Legend',
            height=600,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        # Display in Streamlit
        st.markdown('<h2 class="custom-subheader">Hourly Steps in August</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
            
    
    # Calculate the total and average number of steps per member
    total_steps_per_member = filtered_df.groupby('member_account_id')['steps'].mean()
    average_steps_per_member = total_steps_per_member.mean()

    # Create the bar chart
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=total_steps_per_member.index,
        y=total_steps_per_member.values,
        name='Total Steps per Member',
        marker_color='#009DAE'
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Member Number',
        yaxis_title='Total Number of Steps',
        legend_title='Legend',
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # Display in Streamlit
    st.markdown('<h2 class="custom-subheader">Total Steps per Member</h2>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)


    # Calculate the total number of steps for each unique distance
    total_steps_per_distance = df.groupby('distance')['steps'].mean().reset_index()

    # Sort the DataFrame by distance to ensure the line chart shows a clear trend
    total_steps_per_distance = total_steps_per_distance.sort_values(by='distance')

    # Create the line chart
    fig = go.Figure()

    # Add line trace
    fig.add_trace(go.Scatter(
        x=total_steps_per_distance['distance'],
        y=total_steps_per_distance['steps'],
        mode='markers',
        name='Total Steps per Distance',
        line=dict(color='#009DAE')
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Distance (m)',
        yaxis_title='Total Number of Steps',
        legend_title='Legend',
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # Display in Streamlit
    st.markdown('<h2 class="custom-subheader">Total Steps per Distance</h2>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)


    # Filter the DataFrame for August 2024
    august_2024_df = df[(df['Year'] == 2024)]

    # Calculate the total steps for each day in August 2024
    daily_steps_august = august_2024_df.groupby('created_timestamp').agg(total_steps=('steps', 'sum')).reset_index()

    # Create the line chart for total steps
    fig = go.Figure()

    # Add line trace for the total steps
    fig.add_trace(go.Scatter(
        x=daily_steps_august['created_timestamp'],
        y=daily_steps_august['total_steps'],
        mode='lines',
        fill='tozeroy', 
        line=dict(color='#009DAE'),
        name='Total Steps'
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Steps',
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # Display in Streamlit
    st.markdown('<h2 class="custom-subheader">Daily Total Steps in August 202</h2>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)