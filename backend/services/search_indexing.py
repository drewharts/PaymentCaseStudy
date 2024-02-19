def create_elasticsearch_index(es):
    index_body = {
        "mappings": {
            "properties": {
                "recipient_name": {"type": "text"},
                "recipient_location": {"type": "text"},
                "hospital_name": {"type": "text"},
                "manufacturer_name": {"type": "text"},
                "product_name": {"type": "text"}
            }
        }
    }

    try:
        es.indices.create(index="general_payments_index", body=index_body)
        print("Elasticsearch index 'general_payments_index' created successfully.")
    except Exception as e:
        print(f"Failed to create Elasticsearch index: {e}")
