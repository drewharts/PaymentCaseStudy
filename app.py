from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.backend.services.api import fetch_csv_download_url
from app.backend.services.database_creation import check_or_create_database
from app.backend.services.download_and_insert import download_and_batch_insert
from config import OPEN_PAYMENTS_API_ENDPOINT
import psycopg2



def create_app():
    app = Flask(__name__, template_folder='app/frontend/templates')

    #check to make sure database and table exist, if not create them
    if not check_or_create_database():
        # Fetch the CSV download URL
        csv_url = fetch_csv_download_url(OPEN_PAYMENTS_API_ENDPOINT)

        # Download and batch insert process
        download_and_batch_insert(csv_url)
    else:
        #check to see if database is updated
        print("Checking if database is updated")

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ =='__main__':
    app = create_app()
    app.run(debug=True)