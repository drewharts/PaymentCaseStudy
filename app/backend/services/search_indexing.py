from elasticsearch import Elasticsearch

es = Elasticsearch()

# going to give elastic search name, location, hospital name, manufacturer name, and product name
index_body = {
  "mappings": {
    "properties": {
      "recipient_name": {
        "type": "text"
      },
      "recipient_location": {
        "type": "text"
      },
      "hospital_name": {
        "type": "text"
      },
      "manufacturer_name": {
        "type": "text"
      },
      "product_name": {
        "type": "text"
      }
    }
  }
}

# creating index
es.indices.create(index="general_payments_index", body=index_body)
