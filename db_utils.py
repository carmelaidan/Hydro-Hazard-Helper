import psycopg2
from config import DB_PARAMS

def execute_query(sql, params=None, fetch=False):
    """Execute a database query and optionally fetch results."""
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if fetch:
                    return cur.fetchall()
                conn.commit()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

def init_db():
    """Initialize the water_levels table."""
    sql = """
    CREATE TABLE IF NOT EXISTS water_levels (
        id SERIAL PRIMARY KEY,
        sensor_id VARCHAR(50) NOT NULL,
        water_level_cm NUMERIC(5, 2) NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    if execute_query(sql):
        print("✅ Table 'water_levels' is ready!")
