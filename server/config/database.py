import psycopg2
from .variables import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL database connected successfully.")
    except Exception as e:
        print("PostgreSQL database error:", str(e))
