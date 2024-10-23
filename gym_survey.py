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
st.markdown('<h2 class = "main-title">WORKFORCE HEALTH AND INSURANCE BEHAVIOUR VIEW</h2>', unsafe_allow_html=True)


# Define colors to match the image
custom_colors = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data

df = pd.read_excel('Eden Care Gym Benefits Survey (Responses).xlsx')

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


# Sidebar filters
st.sidebar.header('Filters')


em_group = st.sidebar.multiselect('Select Employer Group', options=df['Employer group'].unique())

# Apply sidebar filters
if em_group:
    df = df[df['Employer group'].isin(em_group)]



# Determine the filter description
filter_description = ""
if em_group:
    filter_description += f"{', '.join(map(str, em_group))} "

if not filter_description:
    filter_description = "All data"



if not df.empty:  

    # Create 4-column layout for metric cards
    col1, col2, = st.columns(2)

    # Define CSS for the styled boxes
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 5px;
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
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1.2em;
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

     # Calculate metrics

    total_part = len(df)

    display_metric(col1, "Total Participants", total_part)


   
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

# Count the occurrences of each Status
    insurance_counts = df["How important is gym access as part of your health and wellness benefits?"].value_counts().reset_index()
    insurance_counts.columns = ["Importance", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Importance of Gym Access to Participants</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="Importance", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

# Count the occurrences of each Status
    health_counts = df["Have you used or tried to use your gym benefits through Eden Care?"].value_counts().reset_index()
    health_counts.columns = ["Benefits", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Eden Care Gym Benefits Utilization</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(health_counts, names="Benefits", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    cols1, cols2 = st.columns(2)

# Count the occurrences of each Status
    insurance_counts = df["Are you currently a member of a gym?"].value_counts().reset_index()
    insurance_counts.columns = ["member", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Current Gym Members</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="member", values="Count",  template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
# Count the occurrences of each Status
    insurance_counts = df["Specific Gyms"].value_counts().reset_index()
    insurance_counts.columns = ["gyms", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants with specific Gym Choices</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="gyms", values="Count",  template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    coverage_counts_1 = df["Are there any specific gyms you would like to see added to our network"].value_counts().nlargest(5).reset_index()
    coverage_counts_1.columns = ["coverage", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Top 5 Preferred Gyms</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts_1, x="coverage", y="Count", text="Count", template="plotly_white", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Preferred Gyms",
            yaxis_title="Number of Participants",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    coverage_counts_2 = df["What areas would you like us to expand our network in (e.g., Remera, Nyarutarama)?"].value_counts().nlargest(5).reset_index()
    coverage_counts_2.columns = ["expand", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Top 5 Areas For Expansion</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts_2, x="expand", y="Count", text="Count", template="plotly_white",color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Location",
            yaxis_title="Number of Participants",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # Create two columns in the Streamlit app
    cols1, cols2 = st.columns(2)

    # Display the first DataFrame with the specified columns
    with cols1:
            with st.expander("Gym choices"):

                st.write(
                    coverage_counts_1
                    .style
                    .background_gradient(cmap="YlOrBr")
                )

    # Display the second DataFrame with the specified columns
    with cols2:
            with st.expander("Areas of Expansion"):

                st.write(
                    coverage_counts_2
                    .style
                    .background_gradient(cmap="YlOrBr")
                )


    cols1, cols2 = st.columns(2)

# Count the occurrences of each Status
    insurance_counts = df["How often do you currently go to the gym or engage in physical activities?"].value_counts().reset_index()
    insurance_counts.columns = ["member", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants Rate of Activity</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="member", values="Count",  template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


# Count the occurrences of each Status
    insurance_counts = df["How much would you be willing to pay for gym access through Eden Care's partnerships?"].value_counts().reset_index()
    insurance_counts.columns = ["amount", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants Gym Payment Rate</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="amount", values="Count",  template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)




    # Count the occurrences of each Status
    coverage_counts_2 = df["What motivates you most to stay fit and healthy?"].value_counts().reset_index()
    coverage_counts_2.columns = ["expand", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants Motivation for Fitness</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts_2, x="expand", y="Count", text="Count", template="plotly_white",color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Mortivation",
            yaxis_title="Number of Participants",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

# Count the occurrences of each Status
    insurance_counts = df["Would you like to claim your gym coupon for Highlands Suites?"].value_counts().reset_index()
    insurance_counts.columns = ["choice", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants Willingness to Claim gym Coupon for Highland Suites</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="choice", values="Count",  template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    coverage_counts_2 = df["What types of rewards would you like to see in our reward redemption program?"].value_counts().reset_index()
    coverage_counts_2.columns = ["expand", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Participants Preferred Reward</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts_2, x="expand", y="Count", text="Count", template="plotly_white",color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Reward",
            yaxis_title="Number of Participants",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)