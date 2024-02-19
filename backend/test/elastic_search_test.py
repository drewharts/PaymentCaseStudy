from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch(["localhost:9200"])

def check_elasticsearch_data():
    try:
        # Search for documents in the specified index
        res = es.search(index="general_payments_index", size=10)  # Adjust size as needed
        hits = res['hits']['hits']

        if hits:
            documents = [hit['_source'] for hit in hits]
            print("Documents found in Elasticsearch:")
            for document in documents:
                print(document)
        else:
            print("No documents found in Elasticsearch.")
    except Exception as e:
        print(f"Error: {e}")

# Run the Elasticsearch data check
if __name__ == '__main__':
    check_elasticsearch_data()
