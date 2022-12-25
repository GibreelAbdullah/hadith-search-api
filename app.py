import sqlite3
from flask_cors import CORS

from flask import Flask, request
from query import *

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('hadith_search_full.db', check_same_thread=False)

def getQuery(query, lang):
    langFilter = ''
    if (lang is not None):
        langFilter = f'AND "language" MATCH "{lang.replace(","," OR ")}"'
    base_query = f"""select
        highlight(hadith,
        0 ,
        '<span style="color:red;">',
        '</span>') hadithnumber ,
        highlight(hadith,
        1 ,
        '<span style="color:red;">',
        '</span>') arabicnumber ,
        highlight(hadith,
        2 ,
        '<span style="color:red;">',
        '</span>') "text" ,
        highlight(hadith,
        3 ,
        '<span style="color:red;">',
        '</span>') grades ,
        highlight(hadith,
        4 ,
        '<span style="color:red;">',
        '</span>') bookNumber ,
        highlight(hadith,
        5 ,
        '<span style="color:red;">',
        '</span>') bookhadith ,
        highlight(hadith,
        6 ,
        '<span style="color:red;">',
        '</span>') bookname ,
        language,
        shortname
    from
        hadith
    WHERE hadith
    MATCH  "{query}"
    and text != ""
    and text != "empty"
    {langFilter}
    order by
        rank
    LIMIT 500"""
    return base_query

@app.route('/search', methods=['GET'])
def searchHadith():
    queryParam = request.args.get("q")
    if (queryParam is None or queryParam == ''):
        return 'Invalid search word'
    elif(conn):
        query = getQuery(queryParam, request.args.get("lang"))
        cursor = conn.execute(query)
        data = cursor.fetchall()
        return data

@app.route('/random', methods=['GET'])
def randomHadith():
    cursor = conn.execute(randomQuery)
    data = cursor.fetchall()
    return data

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    # port = int(os.environ.get('PORT', 5000))
    # # serve(app, host="0.0.0.0", port=port)
    # app.run(debug=True, host='0.0.0.0', port=port)

