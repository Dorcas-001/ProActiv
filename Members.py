
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
        color: #009DAE;
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
st.markdown('<h1 class = "main-title">MEMBER DISTRIBUTION VIEW</h1>', unsafe_allow_html=True)

df = pd.read_excel('proactiv_members.xlsx')
# Ensure the 'Start Date' column is in datetime format if needed
df["Start Date"] = pd.to_datetime(df["Start Date"], errors='coerce')


# Get minimum and maximum dates for the date input
startDate = df["Start Date"].min()
endDate = df["Start Date"].max()

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
df = df[(df["Start Date"] >= date1) & (df["Start Date"] <= date2)].copy()

# Define colors to match the image
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data

# Replace this with your actual data loading method

# Convert 'Date of Birth' to datetime
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'], errors='coerce')

# Drop rows with invalid dates or future dates
today = pd.to_datetime('today')
df = df[df['Date of Birth'] <= today]

# Calculate the age
df['Age'] = today.year - df['Date of Birth'].dt.year

# Create a boolean mask for birthdays that have not occurred yet this year
not_yet_birthday = (today.month < df['Date of Birth'].dt.month) | (
    (today.month == df['Date of Birth'].dt.month) & (today.day < df['Date of Birth'].dt.day)
)

# Subtract 1 from age where the birthday has not yet occurred this year
df.loc[not_yet_birthday, 'Age'] -= 1

# Ensure no negative ages
df['Age'] = df['Age'].clip(lower=0)

# Define CSS for styling
st.markdown("""
    <style>
    .main-title {
        color: #E66C37;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: .5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .slider-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .slider-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
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
        color: #E66C37;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #009DAE;
        font-size: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Slider for age range
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Filter data based on selected age range
filtered_data = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# Sidebar filters
st.sidebar.header('Filters')
# Convert date columns to datetime format
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}

# Year filter
filtered_data['Year'] = filtered_data['Start Date'].dt.year
filtered_data['Month'] = filtered_data['Start Date'].dt.strftime('%B')
sorted_months = sorted(filtered_data['Month'].dropna().unique(), key=lambda x: month_order[x])
# Sidebar filters

year = st.sidebar.multiselect('Select Year', options=sorted(filtered_data['Year'].unique()))
month = st.sidebar.multiselect('Select Month', options=sorted_months)
selected_plan = st.sidebar.multiselect('Select Plan', options=filtered_data['Plan'].unique())
selected_status = st.sidebar.multiselect('Select Status', options=filtered_data['Status'].unique())
selected_em = st.sidebar.multiselect('Select Employer Group', options=filtered_data['Employer'].unique())


# Apply sidebar filters
if year:
    filtered_data = filtered_data[filtered_data['Year'].isin(year)]
if month:
    filtered_data = filtered_data[filtered_data['Month'].isin(month)]
if selected_plan:
    filtered_data = filtered_data[filtered_data['Plan'].isin(selected_plan)]
if selected_status:
    filtered_data = filtered_data[filtered_data['Status'].isin(selected_status)]
if selected_em:
    filtered_data = filtered_data[filtered_data['Employer'].isin(selected_em)]


# Calculate metrics
if not filtered_data.empty:
    total_members = len(filtered_data)
    active_members = len(filtered_data[filtered_data['Status'] == 'Active'])
    unique_members = filtered_data['Employer'].nunique()

    # Display metrics
    col1, col2, col3 = st.columns(3)
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)
    display_metric(col1, "Total Clients", unique_members)
    display_metric(col2, "Total Members", total_members)
    display_metric(col3, "Active Members", active_members)

   
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

    custom_colors = ["#006E7F", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    cols1, cols2 = st.columns(2)

    # Group data by day and count visits
    daily_visits = filtered_data.groupby(filtered_data['Start Date'].dt.to_period('D')).size()
    daily_visits.index = daily_visits.index.to_timestamp()

    # Create a DataFrame for the daily visits
    daily_visits_df = daily_visits.reset_index()
    daily_visits_df.columns = ['Day', 'Number of Workforce']

    with cols1:
        st.markdown('<h3 class="custom-subheader">Number of ProActiv Members Over Time</h3>', unsafe_allow_html=True)

        # Create area chart for visits per day
        fig_area = go.Figure()

        fig_area.add_trace(go.Scatter(
            x=daily_visits_df['Day'],
            y=daily_visits_df['Number of Workforce'],
            fill='tozeroy',
            mode='lines',
            marker=dict(color='#009DAE'),
            line=dict(color='#009DAE'),
            name='Number of Employees'
        ))

        fig_area.update_layout(
            xaxis_title="Days of the Month",
            yaxis_title="Number of Members",
            font=dict(color='black'),
            width=1200, 
            height=460  
        )

        # Display the plot
        st.plotly_chart(fig_area, use_container_width=True)

    # Count the occurrences of each Status
    coverage_counts = filtered_data["Employer"].value_counts().reset_index()
    coverage_counts.columns = ["coverage", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Number of Members by Employer Group</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts, x="coverage", y="Count", text="Count", template="plotly_white", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Employer Group",
            yaxis_title="Number of Members",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    cls1, cls2 = st.columns(2)

    age_counts = filtered_data["Plan"].value_counts().reset_index()
    age_counts.columns = ["plan", "Count"]

    with cls1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Plan Distribution of Members</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(age_counts, names="plan", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
# Count the occurrences of each Status
    gender_counts = filtered_data["Status"].value_counts().reset_index()
    gender_counts.columns = ["Status", "Count"]

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Status Distribution of Members</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(gender_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Create a new column for age groups in 5-year intervals
    filtered_data['Age Group'] = (filtered_data['Age'] // 10) * 10
    filtered_data['Age Group'] = filtered_data['Age Group'].astype(str) + '-' + (filtered_data['Age Group'] + 9).astype(str)

    # Count the occurrences in each age group
    age_counts = filtered_data['Age Group'].value_counts().reset_index()
    age_counts.columns = ['Age Group', 'Count']
    age_counts.columns = ["Age", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Age Distribution of Members</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(age_counts, names="Age", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Group by month and educational background, then count the number of workers
    monthly_workers = filtered_data.groupby(['Year', 'Plan']).size().unstack().fillna(0)

    with cols2:
        fig_monthly_workers = go.Figure()


        for idx, education in enumerate(monthly_workers.columns):
            fig_monthly_workers.add_trace(go.Bar(
                x=monthly_workers.index,
                y=monthly_workers[education],
                name=education,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Workers chart
        fig_monthly_workers.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Year",
            yaxis_title="Number of Members",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Workers chart in Streamlit
        st.markdown('<h3 class="custom-subheader"> Yearly Gender Distribution of ProActiv Members</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_workers, use_container_width=True)


    # Group by month and educational background, then count the number of workers
    monthly_workers = filtered_data.groupby(['Plan', 'Status']).size().unstack().fillna(0)

    # Create the layout columns
    cls1, cls2 = st.columns(2)

    with cls1:
        fig_monthly_workers = go.Figure()


        for idx, education in enumerate(monthly_workers.columns):
            fig_monthly_workers.add_trace(go.Bar(
                x=monthly_workers.index,
                y=monthly_workers[education],
                name=education,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Workers chart
        fig_monthly_workers.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Plan",
            yaxis_title="Number of Members",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Workers chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Plan vs Status Distribution</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_workers, use_container_width=True)

    gender_counts = filtered_data["Employer"].value_counts().reset_index()
    gender_counts.columns = ["employer", "Count"]

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Total ProActiv Client Distribution</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(gender_counts, names="employer", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)