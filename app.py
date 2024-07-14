import sqlite3
import re
from flask_cors import CORS

from flask import Flask, request
from query import *

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('hadith_search_full.db', check_same_thread=False)

def lambda_handler(event, context):
    query_param = event.get('query')
    if not query_param:
        return {'statusCode': 400, 'body': 'Invalid search word'}

    query_param = re.sub(
        r'[\u0000-\u002F \u003A-\u0040 \u005B-\u0060 \u007B-\u007F]', ' ', query_param)
    query_param = re.sub(r'[ ]+', ' OR ', query_param)
    collection = event.get('collection')

    query = searchQuery(query_param, collection)
    cursor = conn.execute(query)
    data = cursor.fetchall()
    return data


if __name__ == '__main__':
    print(lambda_handler({"query": "الرحمن"}, None))


# @app.route('/search', methods=['GET'])
# def searchHadith():
#     queryParam = request.args.get("query")
#     if (queryParam is None or queryParam == ''):
#         return 'Invalid search word'
#     elif(conn):
#         queryParam = re.sub(r'[\u0000-\u002F \u003A-\u0040 \u005B-\u0060 \u007B-\u007F]', ' ',queryParam)
#         queryParam = re.sub(r'[ ]+', ' OR ',queryParam)
#         query = searchQuery(queryParam, request.args.get("language_code"), request.args.get("collection"))
#         # print(query)
#         cursor = conn.execute(query)
#         data = cursor.fetchall()
#         return data

# @app.route('/random', methods=['GET'])
# def randomHadith():
#     length = 99999
#     queryParam = request.args.get("l")
#     if (not(queryParam is None or queryParam == '')):
#         length = int(queryParam)
#     cursor = conn.execute(randomQuery(length))
#     data = cursor.fetchall()
#     return data

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)
    # port = int(os.environ.get('PORT', 5000))
    # # serve(app, host="0.0.0.0", port=port)
    # app.run(debug=True, host='0.0.0.0', port=port)

