import streamlit as st
import requests
import pandas as pd
from config import API_URL

# 1. Setup the page configuration
st.set_page_config(page_title="Hydro-Hazard Dashboard", page_icon="🌊", layout="centered")
st.title("🌊 Automated Hydro-Hazard Helper")
st.subheader("Live Water Level Monitoring")

def fetch_data():
    """Elegantly fetch data from our local Flask API."""
    try:
        response = requests.get(API_URL)
        return response.json().get("data", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to the backend API. Is Flask running?")
        return []

# 2. Fetch and process the data
raw_data = fetch_data()

if raw_data:
    # Pandas elegantly converts our list of dictionaries into a powerful DataFrame table
    df = pd.DataFrame(raw_data)
    
    # 3. Display the most recent reading as a large metric
    latest = df.iloc[0] # Grab the very first row (newest)
    
    # Clever visual logic: If water is above 50cm, show a warning
    status = "⚠️ HIGH WATER" if latest['water_level_cm'] >= 50 else "Normal"
    st.metric(label=f"Latest ({latest['sensor_id']})", 
              value=f"{latest['water_level_cm']} cm", 
              delta=status, delta_color="inverse")
    
    # 4. Visualize the trend with a line chart
    st.subheader("Water Level Trend")
    st.line_chart(df.set_index('recorded_at')['water_level_cm'])
    
    # 5. Show the raw database logs
    st.subheader("Database Logs")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available. Waiting for sensor readings...")

# Add a manual refresh button
if st.button("🔄 Refresh"):
    st.rerun()