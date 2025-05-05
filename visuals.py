"""
visuals.py
Chart and metric rendering for the Jira Work Visualization App.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

def render_metrics(df: pd.DataFrame):
    st.subheader("Key Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Stories", int((df['issue_type'] == 'Story').sum()))
    with col2:
        st.metric("Total Features", int((df['issue_type'] == 'Feature').sum()))
    with col3:
        st.metric("Total Story Points Completed", int(df.loc[df['status'] == 'Done', 'story_points'].sum()))
    with col4:
        avg_time = df.loc[df['resolution_date'].notnull(), 'resolution_date'] - df.loc[df['resolution_date'].notnull(), 'created_date']
        avg_days = avg_time.dt.days.mean() if not avg_time.empty else 0
        st.metric("Avg Time to Resolution (days)", f"{avg_days:.1f}")
    with col5:
        st.metric("Backlog Count", int(((df['status'] == 'To Do') & (df['resolution_date'].isnull())).sum()))
    with col6:
        st.metric("Inventory Count", int((df['status'].isin(['Ready', 'In Progress'])).sum()))

def render_issues_over_time(df: pd.DataFrame):
    st.subheader("Issues Created vs. Resolved Over Time")
    df_created = df.groupby(df['created_date'].dt.to_period('W')).size().reset_index(name='created')
    df_resolved = df[df['resolution_date'].notnull()].groupby(df['resolution_date'].dt.to_period('W')).size().reset_index(name='resolved')
    df_time = pd.merge(df_created, df_resolved, left_on='created_date', right_on='resolution_date', how='outer').fillna(0)
    df_time['week'] = df_time['created_date'].combine_first(df_time['resolution_date']).astype(str)
    fig = px.line(df_time, x='week', y=['created', 'resolved'], markers=True, labels={'value':'Count','week':'Week','variable':'Type'})
    st.plotly_chart(fig, use_container_width=True)

def render_story_points_by_period(df: pd.DataFrame, period: str = 'W'):
    st.subheader(f"Story Points Completed by {'Week' if period=='W' else 'Month'}")
    df_done = df[(df['status'] == 'Done') & (df['resolution_date'].notnull())]
    df_done['period'] = df_done['resolution_date'].dt.to_period(period)
    agg = df_done.groupby('period')['story_points'].sum().reset_index()
    agg['period'] = agg['period'].astype(str)
    fig = px.bar(agg, x='period', y='story_points', labels={'period':'Period','story_points':'Story Points'})
    st.plotly_chart(fig, use_container_width=True)

def render_inventory_by_status(df: pd.DataFrame):
    st.subheader("Current Inventory by Status")
    status_counts = df.groupby('status').size().reset_index(name='count')
    fig = px.pie(status_counts, names='status', values='count', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

def render_backlog_table(df: pd.DataFrame):
    st.subheader("Backlog Items (To Do, unresolved)")
    backlog = df[(df['status'] == 'To Do') & (df['resolution_date'].isnull())]
    st.dataframe(backlog.sort_values(by='created_date'))

def render_inventory_table(df: pd.DataFrame):
    st.subheader("Inventory Items (Ready/In Progress)")
    inventory = df[df['status'].isin(['Ready', 'In Progress'])]
    st.dataframe(inventory.sort_values(by='created_date'))

def render_velocity_trend(df: pd.DataFrame, window: int = 4):
    st.subheader(f"Rolling {window}-Week Velocity Trend")
    df_done = df[(df['status'] == 'Done') & (df['resolution_date'].notnull())]
    df_done = df_done.sort_values('resolution_date')
    df_done['week'] = df_done['resolution_date'].dt.to_period('W')
    weekly = df_done.groupby('week')['story_points'].sum().reset_index()
    weekly['rolling'] = weekly['story_points'].rolling(window=window, min_periods=1).mean()
    weekly['week'] = weekly['week'].astype(str)
    fig = px.line(weekly, x='week', y='rolling', markers=True, labels={'week':'Week','rolling':'Velocity'})
    st.plotly_chart(fig, use_container_width=True)

def render_resolution_histogram(df: pd.DataFrame):
    st.subheader("Time to Resolution Histogram")
    df_res = df[df['resolution_date'].notnull()].copy()
    df_res['resolution_time'] = (df_res['resolution_date'] - df_res['created_date']).dt.days
    fig = px.histogram(df_res, x='resolution_time', nbins=10, labels={'resolution_time':'Days to Resolve'})
    st.plotly_chart(fig, use_container_width=True)
