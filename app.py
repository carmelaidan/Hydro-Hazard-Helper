from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_PARAMS = {
    "dbname": "postgres", "user": "postgres",
    "password": "1546985", "host": "127.0.0.1", "port": "5432"
}

# --- WRITE DOOR (For the ESP32) ---
@app.route('/api/water-level', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        sensor_id = data.get('sensor_id')
        water_level = data.get('water_level_cm')

        if not sensor_id or water_level is None:
            return jsonify({"error": "Missing sensor data"}), 400

        sql_insert = "INSERT INTO water_levels (sensor_id, water_level_cm) VALUES (%s, %s);"
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_insert, (sensor_id, water_level))
                conn.commit()

        return jsonify({"status": "success", "message": "Data saved securely!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- READ DOOR (For the Frontend Dashboard) ---
@app.route('/api/water-level', methods=['GET'])
def get_data():
    try:
        # We elegantly pull only the latest 10 readings to keep the app fast
        sql_select = """
        SELECT id, sensor_id, water_level_cm, recorded_at 
        FROM water_levels 
        ORDER BY recorded_at DESC LIMIT 10;
        """
        
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_select)
                rows = cur.fetchall()
                
        # A clever Python "list comprehension" to instantly map our SQL data into standard JSON format
        results = [
            {
                "id": row[0],
                "sensor_id": row[1],
                "water_level_cm": float(row[2]), # Convert DB numeric to standard float
                "recorded_at": row[3].strftime("%Y-%m-%d %H:%M:%S") # Format the timestamp cleanly
            }
            for row in rows
        ]
        
        return jsonify({"status": "success", "data": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)