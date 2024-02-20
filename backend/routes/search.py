from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch

search_bp = Blueprint('search', __name__)

# Initialize Elasticsearch client
es_search = Elasticsearch(["elasticsearch:9200"])

@search_bp.route('/elasticsearch', methods=['GET'])
def search():
    # Get the query from the request parameters
    query = request.args.get('query')

    # Perform Elasticsearch multi-match query with highlighting
    res = es_search.search(
        index="general_payments_index",
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "best_fields",
                    "fields": ["*"]
                }
            },
            "highlight": {
                "fields": {
                    "*": {}  # Highlight all fields
                }
            }
        }
    )

    # Extract relevant information from search results and include highlights
    hits = res['hits']['hits']
    suggestions = []
    for hit in hits:
        highlight = hit.get('highlight', {})
        highlighted_fields = {}
        for field, value in highlight.items():
            highlighted_fields[field] = value[0] if isinstance(value, list) and value else 'N/A'
        suggestion = {
            'first_name': hit['_source'].get('Covered_Recipient_First_Name', 'N/A'),
            'middle_name': hit['_source'].get('Covered_Recipient_Middle_Name', 'N/A'),
            'last_name': hit['_source'].get('Covered_Recipient_Last_Name', 'N/A'),
            'amount': hit['_source'].get('Total_Amount_of_Payment_USDollars', 'N/A'),
            'id': hit['_source'].get('Record_ID', 'N/A'),
            'highlight': highlighted_fields or 'No highlights'
        }
        suggestions.append(suggestion)

    return jsonify(suggestions)
