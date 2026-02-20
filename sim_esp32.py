import requests

def simulate_sensor():
    # The URL of your local Flask API
    url = "http://127.0.0.1:5000/api/water-level"
    
    # The exact JSON structure our Flask server expects
    payload = {
        "sensor_id": "Ternate_Sensor_02",
        "water_level_cm": 38.2
    }
    
    try:
        # Elegantly send the POST request and capture the server's response
        response = requests.post(url, json=payload, timeout=5)
        
        # Check if the server responded with our 201 Created success code
        if response.status_code == 201:
            print(f"✅ Success! Server replied: {response.json()}")
        else:
            print(f"⚠️ Server error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    simulate_sensor()