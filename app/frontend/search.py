from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch

search_bp = Blueprint('search', __name__)

# Initialize Elasticsearch client
es_search = Elasticsearch(["elasticsearch:9200"])

@search_bp.route('/search', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query')

    # Perform Elasticsearch search with query in the request body
    res = es_search.search(
        index="general_payments_index",
        body={
            "query": {
                "match_phrase_prefix": {
                    "recipient_name": {
                        "query": query,
                        "slop": 10,
                        "max_expansions": 50
                    }
                }
            }
        }
    )

    # Extract relevant information from search results
    hits = res['hits']['hits']
    suggestions = [{'name': hit['_source']['recipient_name']} for hit in hits]

    return jsonify(suggestions)
