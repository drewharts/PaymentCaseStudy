from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS

search_bp = Blueprint('search', __name__)
CORS(search_bp, resources={r"/search": {"origins": "*"}})  # Allow requests from any origin for the /search endpoint

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
                    "fields": ["*"]  # Match on all fields
                }
            }
        }
    )

    # Extract relevant information from search results
    hits = res['hits']['hits']
    suggestions = [{'name': hit['_source']['recipient_name']} for hit in hits]

    return jsonify(suggestions)
