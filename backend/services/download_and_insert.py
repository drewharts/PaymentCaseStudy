import csv
import requests
import psycopg2
from psycopg2 import extras
from elasticsearch import helpers
from services.get_db_connection import get_db_connection


# Define the batch size for processing
BATCH_SIZE = 1
MAX_ROWS_FOR_TESTING = 10

# Placeholder for column length constraints
COLUMN_LENGTHS = {
    'column_name_1': 40,
    'column_name_2': 255,
}


"""
Begins csv download using Python requests, it will then batch downloading data and send to insertion function
"""

def download_and_batch_insert(url, es, encoding='utf-8'):
    try:
        # Connect to the PostgreSQL database
        conn = get_db_connection()
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
                if len(row) == len(headers):
                    # Transform row into a dictionary
                    row_dict = {headers[i]: row[i] for i in range(len(row))}
                    batch.append(row_dict)  # Adjust to append row_dict instead of row
                    row_count += 1
                    if len(batch) >= BATCH_SIZE:
                        insert_batch(cursor, headers, batch, COLUMN_LENGTHS)
                        es_index_batch(batch,es)  # Index batch to Elasticsearch
                        batch = []  # Reset batch after insertion
                        conn.commit()
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


"""
Inserts data from batch provided by download_and_batch_insert into the table
"""
def insert_batch(cursor, headers, batch, column_lengths):
    for row in batch:
        # Validate row against column lengths
        for i, value in enumerate(row.values()):
            header = headers[i]
            max_length = column_lengths.get(header)
            if max_length and len(value) > max_length:
                print(f"Error: Value for column '{header}' exceeds max length of {max_length}. Value: {value}")
                return  # Skip this row or handle as needed

    # If all rows are valid, execute batch insert
    columns = ', '.join(headers)
    placeholders = ', '.join(['%s'] * len(headers))
    values = [tuple(row.get(header) for header in headers) for row in batch]

    sql = f"INSERT INTO general_payments ({columns}) VALUES ({placeholders})"
    try:
        extras.execute_batch(cursor, sql, values)
    except psycopg2.Error as e:
        print(f"Database error during batch insert: {e}")


"""
Takes each batch and sends to Elastic Search
"""

def es_index_batch(batch, es):
    # selected based on what I thought people would be searching for the most
    selected_fields = [
        'Covered_Recipient_Profile_ID', 'Covered_Recipient_NPI',
        'Covered_Recipient_First_Name', 'Covered_Recipient_Middle_Name', 'Covered_Recipient_Last_Name',
        'Recipient_Primary_Business_Street_Address_Line1', 'Recipient_City', 'Recipient_State', 'Recipient_Zip_Code', 'Recipient_Country',
        'Covered_Recipient_Specialty_1',
        'Total_Amount_of_Payment_USDollars', 'Date_of_Payment',
        'Form_of_Payment_or_Transfer_of_Value', 'Nature_of_Payment_or_Transfer_of_Value',
        'Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name',
        'Physician_Ownership_Indicator', 'Contextual_Information',
        'Record_ID', 'Program_Year', 'Payment_Publication_Date'
    ]

    # prepare actions for the Bulk API, only include selected fields
    actions = [
        {
            "_index": "general_payments_index",
            "_id": doc['Record_ID'],  # unique identifier for each document
            "_source": {field: doc[field] for field in selected_fields if field in doc}  # Include only selected fields
        }
        for doc in batch
    ]
    
    try:
        helpers.bulk(es, actions)
        print("Batch indexed successfully.")
    except Exception as e:
        print(f"Error indexing batch in Elasticsearch: {e}")


