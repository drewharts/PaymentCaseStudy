from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch

search_bp = Blueprint('search', __name__)

# Initialize Elasticsearch client
es_search = Elasticsearch(["elasticsearch:9200"])

@search_bp.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query')

    # Perform Elasticsearch multi-match query
    res = es_search.search(
        index="general_payments_index",
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "best_fields",
                    "fields": ["*"]
                }
            }
        }
    )

    # Extract relevant information from search results
    hits = res['hits']['hits']
    suggestions = [{
        'first_name': hit['_source'].get('Covered_Recipient_First_Name', 'N/A'),  # Using .get for safe access
        'middle_name': hit['_source'].get('Covered_Recipient_Middle_Name', 'N/A'),
        'last_name': hit['_source'].get('Covered_Recipient_Last_Name', 'N/A'),
        'hospital_name': hit['_source'].get('Total_Amount_of_Payment_USDollars', 'N/A')
    } for hit in hits]

    return jsonify(suggestions)
