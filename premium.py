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
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
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

# Main title of the dashboard
st.markdown('<h1 class="main-title">PROACTIV PREMIUM VIEW</h1>', unsafe_allow_html=True)

# Load the dataset (replace with your dataset)
df = pd.read_excel('ProActiv Written Premium.xlsx')
df1 = pd.read_excel('ProActiv.xlsx')
df2 = pd.read_csv('reward_redemptions.csv',encoding="ISO-8859-1")

df=pd.concat([df, df1, df2])

# Convert the date column to datetime if necessary
df["Start Date"] = pd.to_datetime(df["Start Date"])

df['Start Year'] = df['Start Year'].astype(int)


month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}
# Create a 'Month-Year' column
df['Month-Year'] = df['Start Month'] + ' ' + df['Start Year'].astype(str)


# Function to sort month-year combinations
def sort_key(month_year):
    month, year = month_year.split()
    return (int(year), month_order[month])

# Extract unique month-year combinations and sort them
month_years = sorted(df['Month-Year'].unique(), key=sort_key)

# Select slider for month-year range
selected_month_year_range = st.select_slider(
    "Select Month-Year Range",
    options=month_years,
    value=(month_years[0], month_years[-1])
)

# Filter DataFrame based on selected month-year range
start_month_year, end_month_year = selected_month_year_range
start_month, start_year = start_month_year.split()
end_month, end_year = end_month_year.split()

start_index = (int(start_year), month_order[start_month])
end_index = (int(end_year), month_order[end_month])

# Filter DataFrame based on month-year order indices
df = df[
    df['Month-Year'].apply(lambda x: (int(x.split()[1]), month_order[x.split()[0]])).between(start_index, end_index)
]


# Sidebar styling and filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Select Year", options=sorted(df['Start Year'].unique()))
month = st.sidebar.multiselect("Select Month", options=sorted(df['Start Month'].unique()))
channel = st.sidebar.multiselect("Select Channel", options=df['Channel'].unique())
channel_name = st.sidebar.multiselect("Select Intermediary name", options=df['Intermediary name'].unique())
em_group = st.sidebar.multiselect("Select Employer Group", options=df['Client Name'].unique())


# Filter data based on user selections
if year:
    df = df[df['Year'].isin(year)]
if month:
    df = df[df['Month'].isin(month)]
if channel:
    df = df[df['channel'].isin(channel)]
if em_group:
    df = df[df['Client Name'].isin(em_group)]
if channel_name:
    df = df[df['Intermediary Name'].isin(channel_name)]


# Calculate total claims, approved claims, rejected claims, and pending claims
scale = 1_000_000
scaled = 1_000
unique_mem = df["Client Name"].nunique()
total_premium = (df["Premium"].sum())/scale
total_lives=df["Total lives"].sum()
av_premium=((df["Premium"].sum())/total_lives)/scaled
total_claims = (df["Claim Amount"].sum())/scale
total_redeems=(df["Item Cost"].sum())/scale
total_cost =  (total_claims+total_redeems)




if not df.empty:
    # Create a 4-column layout for the metrics
    col1, col2, col3, col4= st.columns(4)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

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
                font-size: 1.2em;
                margin-bottom: 10px;
            }
            .metric-value {
                color: #009DAE;
                font-size: 2em;
            }
            </style>
            """, unsafe_allow_html=True)


    # Show total claims, approved claims, rejected claims, and pending claims
    display_metric(col1, "Total Premium", f"{total_premium:.0f} M")
    display_metric(col2, "Total Clients", unique_mem)
    display_metric(col3,"Total Lives Covered",total_lives)
    display_metric(col4, "Average Premium", f"{av_premium:.0f} K")
    display_metric(col1, "Total Claims", f"{total_claims:.1f} M")
    display_metric(col2, "Total Redemptions", f"{total_redeems:.2f} M")
    display_metric(col3,"Total ProActiv Cost",f"{total_cost:.1f} M")



  # Use formatted total claim amount

    custom_colors = ["#006E7F", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    # Visualization for claims by status and top 10 specializations handling claims side by side

    # Create a 2-column layout for the charts
    col1, col2 = st.columns(2)

    # Claims by Status - Pie chart
    with col1:
        st.markdown('<h2 class="custom-subheader">Average Premium By Channel</h2>', unsafe_allow_html=True)
        
        # Sum the claim amount by status
        claim_amount_by_status = df.groupby('Channel')['Average Premium'].sum().reset_index()
        claim_amount_by_status.columns = ['Channel', 'Average Premium']  # Rename columns for clarity

        # Create a pie chart for claim amount by status
        fig = px.pie(
            claim_amount_by_status, 
            names='Channel', 
            values='Average Premium', 
            hole=0.5,
            color_discrete_sequence=custom_colors
        )
        fig.update_layout(
            height=350, 
            margin=dict(l=10, r=10, t=30, b=80)
        )
        fig.update_traces(textposition='inside', textinfo='label+percent+value')
        st.plotly_chart(fig, use_container_width=True)
       
        


    # Group by 'Provider Name' and calculate the mean of 'Claim Amount' and the count of claims
    grouped_df = df.groupby(['Client Name']).agg(
        average_claim_amount=('Premium', 'mean'),
        number_of_claims=('Premium', 'size')
    ).reset_index()

    # Round the 'Claim Amount' to 1 decimal place
    grouped_df['average_claim_amount'] = grouped_df['average_claim_amount'].round(1)

    with col2:
        fig = go.Figure()

        # Add a bar trace for the average claim amount
        fig.add_trace(go.Bar(
            x=grouped_df['Client Name'],
            y=grouped_df['average_claim_amount'],
            name='Average Claim Amount',
            text=grouped_df['average_claim_amount'].apply(lambda x: f'{x:.1f}'),
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE',  # Set the bar color
            yaxis='y1'
        ))



        # Update layout for dual y-axis
        fig.update_layout(
            xaxis_title="Service Provider",
            yaxis=dict(
                title="Average Preium",
                titlefont=dict(color='grey'),
                tickfont=dict(color='grey')
            ),
            yaxis2=dict(
                title="Number of Claims",
                titlefont=dict(color='grey'),
                tickfont=dict(color='grey'),
                overlaying='y',
                side='right'
            ),
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        st.markdown('<h3 class="custom-subheader">Average Premium By Employer Group</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)




    cols1, cols2 = st.columns(2)    
    # Yearly Distribution of Claim Amount - Bar chart
    with cols1:
        st.markdown('<h3 class="custom-subheader">Total Preium By Employer Groups</h3>', unsafe_allow_html=True)
        
        # Group by year and sum the claim amount
        yearly_claim_amount = df.groupby('Start Month')['Premium'].sum().reset_index()
        
        fig_yearly_claims = go.Figure()

        fig_yearly_claims.add_trace(go.Bar(
            x=yearly_claim_amount['Start Month'],
            y=yearly_claim_amount['Premium'],
            name='Total Premium',
            text=yearly_claim_amount['Premium'],
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE'  # Set the bar color
        ))

        # Set layout for the Yearly Claim Amount chart
        fig_yearly_claims.update_layout(
            xaxis_title="Month",
            yaxis_title="Total Premium",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Yearly Claim Amount chart in Streamlit
        st.plotly_chart(fig_yearly_claims, use_container_width=True)
            
       
    # Group by 'Provider Name' and calculate the mean of 'Claim Amount' and the count of claims

     # Yearly Distribution of Claim Amount - Bar chart
    with cols2:
        st.markdown('<h3 class="custom-subheader">Total Lives Covered By Employer Groups</h3>', unsafe_allow_html=True)
        
        # Group by year and sum the claim amount
        yearly_claim_amount = df.groupby('Client Name')['Total lives'].sum().reset_index()
        
        fig_yearly_claims = go.Figure()

        fig_yearly_claims.add_trace(go.Bar(
            x=yearly_claim_amount['Client Name'],
            y=yearly_claim_amount['Total lives'],
            name='Total lives',
            text=yearly_claim_amount['Total lives'],
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE'  # Set the bar color
        ))

        # Set layout for the Yearly Claim Amount chart
        fig_yearly_claims.update_layout(
            xaxis_title="Employer group",
            yaxis_title="Total lives covered",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Yearly Claim Amount chart in Streamlit
        st.plotly_chart(fig_yearly_claims, use_container_width=True)
            
     

     
else:
    st.error("No data available for this selection")