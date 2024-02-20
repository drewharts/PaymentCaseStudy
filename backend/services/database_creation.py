import csv
import requests
from io import StringIO
import psycopg2
import os
from services.get_db_connection import get_db_connection

"""
Connect to default "postgres" database and check if payments database exists. If it doesn't, then create it.
"""
def check_or_create_database():
    try:
        conn = get_db_connection(True)
        conn.autocommit = True
        cursor = conn.cursor()

        #checking if payments database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", ('payments',))
        database_exists = cursor.fetchone()

        if not database_exists:
            cursor.execute("CREATE DATABASE payments;")
            print("Database 'payments' created successfully.")
            execute_sql_schema('models/payment_model.sql')
            return False

        else:
            print("Database 'payments' already exists.")
            return True

    except psycopg2.OperationalError as e:
        print("Error connecting to PostgreSQL:", e)

"""
Connects to 'payments' database and executes SQL mode schema for general payments
"""
def execute_sql_schema(filename):
    with open(filename, 'r') as file:
        sql_commands = file.read()
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql_commands)
        print("Schema executed successfully.")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("Error:", e)
    