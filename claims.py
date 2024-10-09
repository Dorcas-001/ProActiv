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
st.markdown('<h1 class="main-title">MENTAL HEALTH CLAIMS DASHBOARD</h1>', unsafe_allow_html=True)

# Load the dataset (replace with your dataset)
data = pd.read_excel('ProActiv.xlsx')

# Convert the date column to datetime if necessary
data["claim_date"] = pd.to_datetime(data["Claim Created Date"])

# Get min and max dates for the date input
startDate = data["claim_date"].min()
endDate = data["claim_date"].max()
# CSS for date input boxes
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

# 2-column layout for date inputs
col1, col2 = st.columns(2)

def display_date_input(col, title, default_date, min_date, max_date, key):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
    """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date, key=key)

# Display date inputs for filtering
with col1:
    date1 = display_date_input(col1, "Start Date", startDate, startDate, endDate, key="start_date")

with col2:
    date2 = display_date_input(col2, "End Date", endDate, startDate, endDate, key="end_date")

date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)
filtered_data = data[(data["claim_date"] >= date1) & (data["claim_date"] <= date2)].copy()

# Sidebar styling and filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Select Year", options=sorted(filtered_data['Year'].unique()))
month = st.sidebar.multiselect("Select Month", options=sorted(filtered_data['Month'].unique()))
status = st.sidebar.multiselect("Select Claim Status", options=filtered_data['Claim Status'].unique())
em_group = st.sidebar.multiselect("Select Employer Group", options=filtered_data['Employer Name'].unique())
provider = st.sidebar.multiselect("Select Service Provider", options=filtered_data['Provider Name'].unique())


# Filter data based on user selections
if year:
    filtered_data = filtered_data[filtered_data['Year'].isin(year)]
if month:
    filtered_data = filtered_data[filtered_data['Month'].isin(month)]
if status:
    filtered_data = filtered_data[filtered_data['status'].isin(status)]
if em_group:
    filtered_data = filtered_data[filtered_data['Employer Name'].isin(em_group)]
if provider:
    filtered_data = filtered_data[filtered_data['Provider Name'].isin(provider)]


# Calculate total claims, approved claims, rejected claims, and pending claims
active_mem = 80
scale = 1_000_000
total_claims = len(filtered_data)
unique_mem = filtered_data["Member Number"].nunique()
percent_unique = (unique_mem/active_mem) * 100
approved_claim_amount = filtered_data[filtered_data['Claim Status'] == 'Approved']['Approved Claim Amount'].sum() / scale

approved_claims = filtered_data[filtered_data['Claim Status'] == 'Approved'].shape[0]
rejected_claims = filtered_data[filtered_data['Claim Status'] == 'Rejected'].shape[0]
pending_claims = filtered_data[filtered_data['Claim Status'] == 'Pending'].shape[0]
# Calculate total claim amount
total_claim_amount = (filtered_data['Claim Amount'].sum())/scale


if not filtered_data.empty:
    # Create a 4-column layout for the metrics
    col1, col2, col3= st.columns(3)

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
    display_metric(col1, "Total Claims", total_claims)
    display_metric(col2, "Unique Claims", unique_mem)
    display_metric(col3,"Percentage claimed", f"{percent_unique:,.1f}%")
    display_metric(col1, "Approved Claims", approved_claims)
    display_metric(col2, "Total Claim Amount", f"RWF {total_claim_amount:.1f} M")
    display_metric(col3, "Approved Claim Amount", f"RWF {approved_claim_amount:.1f} M")

  # Use formatted total claim amount

    custom_colors = ["#006E7F", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    # Visualization for claims by status and top 10 specializations handling claims side by side

    # Create a 2-column layout for the charts
    col1, col2 = st.columns(2)

    # Claims by Status - Pie chart
    with col1:
        st.markdown('<h2 class="custom-subheader">Claim Amount by Status</h2>', unsafe_allow_html=True)
        
        # Sum the claim amount by status
        claim_amount_by_status = filtered_data.groupby('Claim Status')['Claim Amount'].sum().reset_index()
        claim_amount_by_status.columns = ['status', 'Total Claim Amount']  # Rename columns for clarity

        # Create a pie chart for claim amount by status
        fig = px.pie(
            claim_amount_by_status, 
            names='status', 
            values='Total Claim Amount', 
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            height=350, 
            margin=dict(l=10, r=10, t=30, b=80)
        )
        fig.update_traces(textposition='inside', textinfo='label+percent+value')
        st.plotly_chart(fig, use_container_width=True)
       
        


    # Group by 'Provider Name' and calculate the mean of 'Claim Amount' and the count of claims
    grouped_df = filtered_data.groupby(['Provider Name']).agg(
        average_claim_amount=('Claim Amount', 'mean'),
        number_of_claims=('Claim Amount', 'size')
    ).reset_index()

    # Round the 'Claim Amount' to 1 decimal place
    grouped_df['average_claim_amount'] = grouped_df['average_claim_amount'].round(1)

    with col2:
        fig = go.Figure()

        # Add a bar trace for the average claim amount
        fig.add_trace(go.Bar(
            x=grouped_df['Provider Name'],
            y=grouped_df['average_claim_amount'],
            name='Average Claim Amount',
            text=grouped_df['average_claim_amount'].apply(lambda x: f'{x:.1f}'),
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE',  # Set the bar color
            yaxis='y1'
        ))

        # Add a line trace for the number of claims
        fig.add_trace(go.Scatter(
            x=grouped_df['Provider Name'],
            y=grouped_df['number_of_claims'],
            name='Number of Claims',
            text=grouped_df['number_of_claims'],
            textposition='top center',
            textfont=dict(color='black'),
            hoverinfo='x+y+name',
            marker_color='#FF5733',  # Set the line color
            yaxis='y2'
        ))

        # Update layout for dual y-axis
        fig.update_layout(
            xaxis_title="Service Provider",
            yaxis=dict(
                title="Average Claim Amount",
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

        st.markdown('<h3 class="custom-subheader">Average Claim Amount and Number of Claims by Provider</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)


    # Group by 'Provider Name' and calculate the mean of 'Claim Amount' and the count of claims
    grouped_df = filtered_data.groupby(['Employer Name']).agg(
        average_claim_amount=('Claim Amount', 'mean'),
        number_of_claims=('Claim Amount', 'size')
    ).reset_index()

    # Round the 'Claim Amount' to 1 decimal place
    grouped_df['average_claim_amount'] = grouped_df['average_claim_amount'].round(1)

    with col1:
        fig = go.Figure()

        # Add a bar trace for the average claim amount
        fig.add_trace(go.Bar(
            x=grouped_df['Employer Name'],
            y=grouped_df['average_claim_amount'],
            name='Average Claim Amount',
            text=grouped_df['average_claim_amount'].apply(lambda x: f'{x:.1f}'),
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE',  # Set the bar color
            yaxis='y1'
        ))

        # Add a line trace for the number of claims
        fig.add_trace(go.Scatter(
            x=grouped_df['Employer Name'],
            y=grouped_df['number_of_claims'],
            name='Number of Claims',
            text=grouped_df['number_of_claims'],
            textposition='top center',
            textfont=dict(color='black'),
            hoverinfo='x+y+name',
            marker_color='#FF5733',  # Set the line color
            yaxis='y2'
        ))

        # Update layout for dual y-axis
        fig.update_layout(
            xaxis_title="Service Provider",
            yaxis=dict(
                title="Average Claim Amount",
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

        st.markdown('<h3 class="custom-subheader">Average Claim Amount and Number of Claims by Employer</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

    cols1, cols2 = st.columns(2)    
    # Yearly Distribution of Claim Amount - Bar chart
    with col2:
        st.markdown('<h3 class="custom-subheader">Monthly Distribution of Claim Amount</h3>', unsafe_allow_html=True)
        
        # Group by year and sum the claim amount
        yearly_claim_amount = filtered_data.groupby('Month')['Claim Amount'].sum().reset_index()
        
        fig_yearly_claims = go.Figure()

        fig_yearly_claims.add_trace(go.Bar(
            x=yearly_claim_amount['Month'],
            y=yearly_claim_amount['Claim Amount'],
            name='Total Claim Amount',
            text=yearly_claim_amount['Claim Amount'],
            textposition='inside',
            textfont=dict(color='white'),
            hoverinfo='x+y+name',
            marker_color='#009DAE'  # Set the bar color
        ))

        # Set layout for the Yearly Claim Amount chart
        fig_yearly_claims.update_layout(
            xaxis_title="Month",
            yaxis_title="Total Claim Amount",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Yearly Claim Amount chart in Streamlit
        st.plotly_chart(fig_yearly_claims, use_container_width=True)
            
       
       
     
else:
    st.error("No data available for this selection")