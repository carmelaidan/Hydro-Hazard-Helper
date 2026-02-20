import psycopg2

def create_table():
    db_params = {
        "dbname": "postgres", "user": "postgres",
        "password": "1546985", "host": "127.0.0.1", "port": "5432"
    }

    # Our elegant SQL command to create the table if it doesn't already exist.
    sql_query = """
    CREATE TABLE IF NOT EXISTS water_levels (
        id SERIAL PRIMARY KEY,
        sensor_id VARCHAR(50) NOT NULL,
        water_level_cm NUMERIC(5, 2) NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        # Using context managers ('with') to keep our execution clean and safe
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
        print("✅ Table 'water_levels' is ready for data!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_table()