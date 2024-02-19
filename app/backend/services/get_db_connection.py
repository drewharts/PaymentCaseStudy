import os
import psycopg2
"""
Grabs connection with environment variables for best practice
"""
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'payments'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', 'password'), 
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn
