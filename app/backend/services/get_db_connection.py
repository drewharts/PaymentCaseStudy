import os
import psycopg2

def get_db_connection(default=False):
    if default:
        dbname = 'postgres'
    else:
        dbname = os.getenv('DB_NAME', 'payments')
        
    conn = psycopg2.connect(
        dbname=dbname,
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', 'password'), 
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn
