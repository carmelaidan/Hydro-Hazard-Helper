import streamlit as st
import requests
import pandas as pd

# 1. Setup the page configuration
st.set_page_config(page_title="Hydro-Hazard Dashboard", page_icon="🌊", layout="centered")
st.title("🌊 Automated Hydro-Hazard Helper")
st.subheader("Live Water Level Monitoring")

API_URL = "http://127.0.0.1:5000/api/water-level"

def fetch_data():
    """Elegantly fetch data from our local Flask API."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json().get("data", [])
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
    status = "Normal" if latest['water_level_cm'] < 50 else "⚠️ HIGH WATER"
    st.metric(label=f"Latest Reading ({latest['sensor_id']})", 
              value=f"{latest['water_level_cm']} cm", 
              delta=status, delta_color="inverse" if status == "Normal" else "normal")
    
    # 4. Visualize the trend with a line chart
    st.write("### Water Level Trend")
    # Set the timestamp as the X-axis, and graph the water level
    chart_data = df.set_index('recorded_at')['water_level_cm']
    st.line_chart(chart_data)
    
    # 5. Show the raw database logs
    st.write("### Database Logs")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("No data found. Waiting for sensor transmissions...")

# Add a manual refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()