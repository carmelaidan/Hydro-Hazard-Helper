import psycopg2
from config import DB_PARAMS

try:
    with psycopg2.connect(**DB_PARAMS) as conn:
        print("✅ Successfully connected to PostgreSQL!")
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")