import csv
import requests
import psycopg2
from psycopg2 import extras
from .api import fetch_csv_download_url
from config import OPEN_PAYMENTS_API_ENDPOINT, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Define the batch size for processing
BATCH_SIZE = 1000
MAX_ROWS_FOR_TESTING = 100

# Placeholder for column length constraints
COLUMN_LENGTHS = {
    'column_name_1': 40,
    'column_name_2': 255,
}

def download_and_batch_insert(url, encoding='utf-8'):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        # Disable autocommit for batch transaction
        conn.autocommit = False
        cursor = conn.cursor()

        # Initialize batch list
        batch = []
        row_count = 0

        # Start streaming the CSV from the URL
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            lines = (line.decode(encoding) for line in r.iter_lines())
            csv_reader = csv.reader(lines)
            headers = next(csv_reader)  # Assuming the first row is the header

            for row in csv_reader:
                if len(row) == len(headers):  # Ensure row has correct number of columns
                    row_count += 1
                    batch.append(row)
                    if len(batch) >= BATCH_SIZE:
                        insert_batch(cursor, headers, batch, COLUMN_LENGTHS)
                        batch = []  # Reset batch after insertion
                        conn.commit()  # Commit the transaction after each batch insert
                    if row_count >= MAX_ROWS_FOR_TESTING:
                        break

            # Insert any remaining rows in the batch
            if batch:
                insert_batch(cursor, headers, batch, COLUMN_LENGTHS)
                conn.commit()

        print("Data insertion completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback transaction on error
    finally:
        cursor.close()
        conn.close()

def insert_batch(cursor, headers, batch, column_lengths):
    for row in batch:
        # Validate row against column lengths
        for i, value in enumerate(row):
            header = headers[i]
            max_length = column_lengths.get(header)
            if max_length and len(value) > max_length:
                print(f"Error: Value for column '{header}' exceeds max length of {max_length}. Value: {value}")
                return  # Skip this row or handle as needed

    # If all rows are valid, execute batch insert
    columns = ', '.join(headers)
    placeholders = ', '.join(['%s'] * len(headers))
    sql = f"INSERT INTO general_payments ({columns}) VALUES ({placeholders})"
    try:
        extras.execute_batch(cursor, sql, batch)
    except psycopg2.Error as e:
        print(f"Database error during batch insert: {e}")
