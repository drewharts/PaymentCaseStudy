from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.backend.services.api import fetch_csv_download_url
from app.backend.services.downloadInsert import check_or_create_database
import psycopg2

app = Flask(__name__, template_folder='app/frontend/templates')


check_or_create_database()



#defining API endpoint here
api_endpoint = "https://openpaymentsdata.cms.gov/api/1/metastore/schemas/dataset/items/df01c2f8-dc1f-4e79-96cb-8208beaf143c?show-reference-ids=false"

fetch_csv_download_url(api_endpoint)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ =='__main__':
    app.run(debug=True)