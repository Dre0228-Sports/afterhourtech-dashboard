import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Afterhourtech Sports Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🏆 Afterhourtech Sports Dashboard")
st.markdown("---")

# Load sample data
@st.cache_data
def load_data():
    data = {
        'Date': ['2026-04-02', '2026-04-02', '2026-04-01', '2026-04-01'],
        'Sport': ['NBA', 'MLB', 'NBA', 'NHL'],
        'Pick': ['Anthony Edwards OVER 26.5 Points', 'Houston Astros ML', 'Jayson Tatum OVER 28.5 Points', 'Auston Matthews OVER 0.5 Goals'],
        'Confidence': ['A+', 'A+', 'A+', 'A'],
        'Status': ['Pending', 'Pending', 'Hit', 'Hit'],
        'Line': [-110, -125, -110, -120]
    }
    return pd.DataFrame(data)

df = load_data()

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Picks", len(df))
with col2:
    hits = len(df[df['Status'] == 'Hit'])
    st.metric("Hits", hits)
with col3:
    win_rate = (hits / len(df[df['Status'] != 'Pending'])) * 100 if len(df[df['Status'] != 'Pending']) > 0 else 0
    st.metric("Win Rate", f"{win_rate:.1f}%")
with col4:
    st.metric("A+ Picks", len(df[df['Confidence'] == 'A+']))

st.markdown("---")

# Recent picks
st.subheader("📈 Recent Picks")
for _, row in df.iterrows():
    status_color = "🟢" if row['Status'] == 'Hit' else "🟡" if row['Status'] == 'Pending' else "🔴"
    st.write(f"{status_color} **{row['Pick']}** | {row['Sport']} | {row['Confidence']} | {row['Status']}")

# Charts
st.subheader("📊 Performance Analytics")

col1, col2 = st.columns(2)

with col1:
    # Win rate by sport
    sport_stats = df[df['Status'] != 'Pending'].groupby('Sport')['Status'].apply(lambda x: (x == 'Hit').mean() * 100).reset_index()
    sport_stats.columns = ['Sport', 'Win_Rate']
    
    if not sport_stats.empty:
        fig = px.bar(sport_stats, x='Sport', y='Win_Rate', title="Win Rate by Sport")
        st.plotly_chart
