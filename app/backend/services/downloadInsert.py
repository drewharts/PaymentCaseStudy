import csv
import requests
from io import StringIO
import psycopg2

def check_or_create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to the default "postgres" database
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", ('payments',))
        database_exists = cursor.fetchone()

        if not database_exists:
            cursor.execute("CREATE DATABASE payments;")
            print("Database 'payments' created successfully.")
            execute_sql_schema('app/backend/models/payment_model.sql',dbname='payments')

        else:
            print("Database 'payments' already exists.")

        cursor.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print("Error connecting to PostgreSQL:", e)

def execute_sql_schema(filename,dbname):
    with open(filename, 'r') as file:
        sql_commands = file.read()
    try:
        conn = psycopg2.connect(
            dbname=dbname,  # Connect to the 'payments' database
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql_commands)
        print("Schema executed successfully.")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("Error:", e)


def download_and_insert(url, db_connection):
    with requests.get(url,stream=True) as r:
        r.raise_for_status()

        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()

        partial_chunk = ""

        for chunk in r.iter_content(chunk_size=1024*1024, decode_unicode=True):
            combined_chunk = partial_chunk + chunk

            if combined_chunk.endswith('\n'):
                #create function here to insert
                proccess_chunk(combined_chunk,cursor)
                partial_chunk = ""
            else:
                # If not ending with a newline, find the last newline and process up to it
                last_newline_idx = combined_chunk.rfind('\n')
                # Process up to the last complete row
                process_chunk(combined_chunk[:last_newline_idx], cursor)
                # Save the remaining partial row for the next iteration
                partial_chunk = combined_chunk[last_newline_idx+1:]

        if partial_chunk:
            process_chunk(partial_chunk + '\n',cursor)
        
        conn.commit()
        cursor.close()
        conn.close()


# def process_chunk(chunk,cursor):
    