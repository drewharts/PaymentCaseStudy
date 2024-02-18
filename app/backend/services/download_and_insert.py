import csv
import requests
import psycopg2
from psycopg2 import extras
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from elasticsearch import Elasticsearch, helpers

# Define the batch size for processing
BATCH_SIZE = 1000
MAX_ROWS_FOR_TESTING = 100

# Placeholder for column length constraints
COLUMN_LENGTHS = {
    'column_name_1': 40,
    'column_name_2': 255,
}

#Elastic Search Client
es = Elasticsearch(
    hosts=["localhost:9200"],
    http_auth=('username', 'password')
)


"""
Begins csv download using Python requests, it will then batch downloading data and send to insertion function
"""

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
                if len(row) == len(headers):
                    # Transform row into a dictionary
                    row_dict = {headers[i]: row[i] for i in range(len(row))}
                    batch.append(row_dict)  # Adjust to append row_dict instead of row
                    row_count += 1
                    if len(batch) >= BATCH_SIZE:
                        insert_batch(cursor, headers, batch, COLUMN_LENGTHS)
                        es_index_batch(batch)  # Index batch to Elasticsearch
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

"""
Takes each batch and sends to Elastic Search
"""
def es_index_batch(batch):
    # Prepare actions for the Bulk API
    actions = [
        {
            "_index": "general_payments_index",
            "_id": doc['Record_ID'],  # Use the unique identifier for each document
            "_source": {
                "recipient_name": f"{doc.get('Covered_Recipient_First_Name', '')} {doc.get('Covered_Recipient_Last_Name', '')}",
                "recipient_location": f"{doc.get('Recipient_City', '')}, {doc.get('Recipient_State', '')}, {doc.get('Recipient_Country', '')}",
                "hospital_name": doc.get('Teaching_Hospital_Name', ''),
                "manufacturer_name": doc.get('Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name', ''),
                "product_name": doc.get('Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1', '')  # Adjust as necessary
                # Add more fields from doc as necessary
            }
        }
        for doc in batch
    ]
    
    try:
        helpers.bulk(es, actions)
    except Exception as e:
        print(f"Error indexing batch in Elasticsearch: {e}")
