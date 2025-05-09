"""
app.py
Main Streamlit app for Jira Work Visualization and Insights
"""
import streamlit as st
import pandas as pd
from data_loader import load_jira_data
import visuals

st.set_page_config(
    page_title="Jira Work Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Jira Work Visualization & Insights Dashboard")
st.markdown("""
A modern, interactive dashboard for tracking Jira Features and Stories.
""")

# Load data
data = load_jira_data()

# Sidebar filters
st.sidebar.header("Filters")
# Date range
min_date = data['created_date'].min()
max_date = data['created_date'].max()
date_range = st.sidebar.date_input(
    "Created Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
# Issue Type
issue_types = ["All"] + sorted(data['issue_type'].dropna().unique().tolist())
issue_type = st.sidebar.selectbox("Issue Type", issue_types)
# Status
statuses = sorted(data['status'].dropna().unique().tolist())
status_select = st.sidebar.multiselect("Status", statuses, default=statuses)
# Program
programs = ["All"] + sorted(data['Program'].dropna().unique().tolist())
program_select = st.sidebar.selectbox("Program", programs)
# ProjectName
projects = ["All"] + sorted(data['ProjectName'].dropna().unique().tolist())
project_select = st.sidebar.selectbox("Project Name", projects)

# Filter data
filtered = data.copy()
if date_range:
    filtered = filtered[(filtered['created_date'] >= pd.to_datetime(date_range[0])) & (filtered['created_date'] <= pd.to_datetime(date_range[1]))]
if issue_type != "All":
    filtered = filtered[filtered['issue_type'] == issue_type]
if status_select:
    filtered = filtered[filtered['status'].isin(status_select)]
if program_select != "All":
    filtered = filtered[filtered['Program'] == program_select]
if project_select != "All":
    filtered = filtered[filtered['ProjectName'] == project_select]

# Main dashboard
visuals.render_metrics(filtered)

col1, col2 = st.columns(2)
with col1:
    visuals.render_issues_over_time(filtered)
with col2:
    visuals.render_story_points_by_period(filtered, period='W')

col3, col4 = st.columns(2)
with col3:
    visuals.render_inventory_by_status(filtered)
with col4:
    visuals.render_velocity_trend(filtered, window=4)

visuals.render_resolution_histogram(filtered)

# Backlog and Inventory tables
st.markdown("---")
st.header("Backlog & Inventory Analysis")
col5, col6 = st.columns(2)
with col5:
    visuals.render_backlog_table(filtered)
with col6:
    visuals.render_inventory_table(filtered)

# Gantt Chart Visualization
st.markdown("---")
st.header("Project Timeline (Gantt Chart)")
visuals.render_gantt_chart(filtered)

st.caption("Built with Streamlit and Plotly.")
