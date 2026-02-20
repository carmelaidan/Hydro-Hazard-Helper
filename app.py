from flask import Flask, request, jsonify
import psycopg2
from config import DB_PARAMS

app = Flask(__name__)

@app.route('/api/water-level', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        sensor_id, water_level = data.get('sensor_id'), data.get('water_level_cm')
        
        if not sensor_id or water_level is None:
            return jsonify({"error": "Missing sensor data"}), 400

        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO water_levels (sensor_id, water_level_cm) VALUES (%s, %s);", 
                           (sensor_id, water_level))
                conn.commit()
        
        return jsonify({"status": "success", "message": "Data saved!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/water-level', methods=['GET'])
def get_data():
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, sensor_id, water_level_cm, recorded_at 
                    FROM water_levels ORDER BY recorded_at DESC LIMIT 10;
                """)
                rows = cur.fetchall()
        
        results = [{
            "id": row[0],
            "sensor_id": row[1],
            "water_level_cm": float(row[2]),
            "recorded_at": row[3].strftime("%Y-%m-%d %H:%M:%S")
        } for row in rows]
        
        return jsonify({"status": "success", "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)