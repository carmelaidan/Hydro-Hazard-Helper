from db_utils import execute_query
import psycopg2
from config import DB_PARAMS

sql = "INSERT INTO water_levels (sensor_id, water_level_cm) VALUES (%s, %s) RETURNING id, recorded_at;"

try:
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, ("Ternate_Sensor_01", 45.5))
            new_id, timestamp = cur.fetchone()
            conn.commit()
    print(f"✅ Success! Saved reading #{new_id} at {timestamp}")
except Exception as e:
    print(f"❌ Error: {e}")