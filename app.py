import os
import sqlite3
from flask_cors import CORS

# from waitress import serve
from flask import Flask, request

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('hadith_search_full.db', check_same_thread=False)

def getQuery(query, lang):
    langFilter = ''
    print(lang)
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
        '</span>') "text" ,
        highlight(hadith,
        2 ,
        '<span style="color:red;">',
        '</span>') grades ,
        highlight(hadith,
        3 ,
        '<span style="color:red;">',
        '</span>') bookNumber ,
        highlight(hadith,
        4 ,
        '<span style="color:red;">',
        '</span>') bookhadith ,
        highlight(hadith,
        5 ,
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
    LIMIT 200"""
    print(base_query)
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
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # serve(app, host="0.0.0.0", port=port)
    app.run(debug=True, host='0.0.0.0', port=port)

