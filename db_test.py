import psycopg2
from psycopg2 import OperationalError

def test_connection():
    # Dictionary storing your database credentials. 
    # UPDATE 'password' to the one you set when installing PostgreSQL.
    db_params = {
        "dbname": "postgres", 
        "user": "postgres",
        "password": "1546985",
        "host": "127.0.0.1",
        "port": "5432"
    }

    try:
        # The '**' elegantly unpacks the dictionary into connection arguments.
        # The 'with' statement safely handles the connection and closes it automatically.
        with psycopg2.connect(**db_params) as conn:
            print("✅ Successfully connected to the PostgreSQL database!")
            
    except OperationalError as e:
        print(f"❌ Connection failed. Check your password and ensure PostgreSQL is running.\nError Details: {e}")

if __name__ == "__main__":
    test_connection()