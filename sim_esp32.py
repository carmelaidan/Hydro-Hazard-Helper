import requests
from config import API_URL

try:
    response = requests.post(API_URL, json={
        "sensor_id": "Ternate_Sensor_02",
        "water_level_cm": 38.2
    }, timeout=5)
    
    if response.status_code == 201:
        print(f"✅ Success! {response.json()}")
    else:
        print(f"⚠️ Error {response.status_code}: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"❌ Connection failed: {e}")