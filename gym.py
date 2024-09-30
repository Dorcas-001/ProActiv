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
st.markdown('<h1 class = "main-title">Reward Redemption Dashboard</h1>', unsafe_allow_html=True)
# Loading the data
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']

@st.cache_data
def load_data():
    data = pd.read_excel('Active-Lives.xlsx')
    data['Start Date'] = pd.to_datetime(data['Start Date'])
    data['Year'] = data['Start Date'].dt.year
    data['Month'] = data['Start Date'].dt.strftime('%b')
    return data

data = load_data()

# Get minimum and maximum dates for the date input
startDate = data["Start Date"].min()
endDate = data["Start Date"].max()

# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create 2-column layout for date inputs
col1, col2 = st.columns(2)

# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)

# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))
with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))

# Filter DataFrame based on the selected dates
df = data[(data["Start Date"] >= date1) & (data["Start Date"] <= date2)].copy()

# Sidebar
st.sidebar.header('Filters')

# Ensure 'Month' column contains only strings
data['Month'] = data['Month'].astype(str)

selected_year = st.sidebar.multiselect('Select Year', options=sorted(data['Year'].unique()))
selected_month = st.sidebar.multiselect('Select Month', options=sorted(data['Month'].unique()))
selected_merchants = st.sidebar.multiselect('Select Employer group', options=data['Employer Name'].unique())


filtered_data = data
if selected_year:
    filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]
if selected_month:
    filtered_data = filtered_data[filtered_data['Month'].isin(selected_month)]
if selected_merchants:
    filtered_data = filtered_data[filtered_data['Employer Name'].isin(selected_merchants)]

filter_description = ""
if selected_year:
    filter_description += f"{', '.join(map(str, selected_year))} "

if selected_month:
    filter_description += f"{', '.join(map(str, selected_month))} "

if selected_merchants:
    filter_description += f"{', '.join(selected_merchants)} "

if not filter_description:
    filter_description = "All Data"

# Calculate Metrics
total_member = len(filtered_data)
active_mem = 7388
unique_mem = filtered_data["Member Number"].nunique()
percent_unique = (unique_mem/active_mem) * 100

if not filtered_data.empty:
    # Top metrics

    st.markdown("""
        <style>
        .custom-subheader {
            color: #E66C37;
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
            color: #E66C37; /* Change this color to your preferred title color */
            font-size: 0.8em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1.5em;
        }
        </style>
        """, unsafe_allow_html=True)
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
        

    # Display Metrics Side by Side
    col1, col2, col3 = st.columns(3)
    display_metric(col1,"Total Members", total_member)
    display_metric(col2,"Total Unique Gym Members", unique_mem)
    display_metric(col3,"Percentage Gym members", f"{percent_unique:,.1f}%")


    cols1, cols2 = st.columns(2)
    # Convert 'Start Date' to datetime
    data['Start Date'] = pd.to_datetime(data['Start Date'])

        # Set 'Start Date' as the index
    data.set_index('Start Date', inplace=True)

    # Sort the DataFrame by the index
    data.sort_index(inplace=True)

    # Create the time series for the count of 'Member Number'
    time_series_data = data.groupby(data.index).agg(member_count=('Member Number', 'count')).reset_index()


    # Group the data by Year and Month, counting the number of unique Member IDs
    df_grouped = filtered_data.groupby(['Year', 'Month'], as_index=False)['Member Number'].nunique()

    # Define the order of months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_grouped['Month'] = pd.Categorical(df_grouped['Month'], categories=month_order, ordered=True)

    with cols1:
        # Create the bar chart
        fig_members = px.bar(df_grouped, x='Month', y='Member Number',
                            labels={'Member Number': 'Number of Members'})

        # Update layout to order the months correctly
        fig_members.update_layout(
            xaxis=dict(categoryorder='array', categoryarray=month_order),
            xaxis_title='Month',
            yaxis_title='Number of Members',
            height=350,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        # Optionally, set a custom color for the bars
        teal_color = '#008080'  # Example color
        fig_members.update_traces(marker_color=teal_color)

        # Display the chart in Streamlit
        st.markdown('<h2 class="custom-subheader">Number of Members Since January</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_members)


    # Create Doughnut Chart
    df_merchant = data.groupby('Gender').size().reset_index(name='Count')


    with cols2:
        fig_doughnut = px.pie(
            df_merchant, 
            names='Gender', 
            values='Count',
            color_discrete_sequence=color_palette,
            hole=0.4  # This creates the doughnut hole
        )
        
        fig_doughnut.update_traces(
            textposition='inside', 
            textinfo='percent+label'
        )
        fig_doughnut.update_layout(
            height=350, 
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True
        )

        # Display the doughnut chart in Streamlit
        st.markdown('<h2 class="custom-subheader">Gender Distribution</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_doughnut, use_container_width=True)

 # Create the line chart for member count
    fig = go.Figure()

        # Add line trace for the member count
    fig.add_trace(go.Scatter(
            x=time_series_data['Start Date'],
            y=time_series_data['member_count'],
            mode='lines',
            fill='tozeroy', 
            line=dict(color='#009DAE'),
            name='Member Count'
        ))

        # Update layout
    fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Members',
            height=600,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        # Display in Streamlit
    st.markdown('<h2 class="custom-subheader">Member Count Over Time</h2>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)  

else:
     st.error("No data available for this selection")