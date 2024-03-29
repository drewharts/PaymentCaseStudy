from flask import Flask, render_template
from services.api import fetch_csv_download_url
from services.database_creation import check_or_create_database
from services.download_and_insert import download_and_batch_insert
from routes.search import search_bp
from routes.getsql import getsql_bp
from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from flask_cors import CORS





def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='templates')

    # Register the search blueprint
    app.register_blueprint(search_bp,url_prefix='/search')
    app.register_blueprint(getsql_bp,url_prefix='/data')

    CORS(app)
    
    es = Elasticsearch(
        hosts=["elasticsearch:9200"]
    )
    

    #check to make sure database and table exist, if not create them
    if not check_or_create_database():
        # Fetch the CSV download URL
        csv_url = fetch_csv_download_url(os.getenv('OPEN_PAYMENTS_API_ENDPOINT'))

        # Download and batch insert process
        download_and_batch_insert(csv_url,es)
    else:
        #check to see if database is updated
        print("Checking if database is updated")

    @app.route('/')
    def home():
        return render_template('index.html')
    

    return app


if __name__ =='__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0',port=8000)

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello, World!'
