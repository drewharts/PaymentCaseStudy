from flask import  request, jsonify, Blueprint
import psycopg2
from psycopg2.extras import RealDictCursor
from services.get_db_connection import get_db_connection
import os

getsql_bp = Blueprint('data',__name__)

@getsql_bp.route('/get-details', methods=['GET'])
def get_details():
    unique_id = str(request.args.get('id'))
    #set to false (not default) to grab from payments database
    conn = get_db_connection(False)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM general_payments WHERE Record_ID = %s", (unique_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)
