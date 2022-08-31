import os

from flask import Flask, jsonify
from google.cloud import datastore


app = Flask(__name__)

datastore_client = datastore.Client()
kind = 'Visit'
name = 'name=num-visits'


def get_counts():
    query = datastore_client.query(kind=kind)
    queries = list(query.fetch())
    queries.sort(key=lambda x : x['count'], reverse=True)
    counts = queries[0]['count']
    return counts


def update_db():
    val = get_counts()
    entity = datastore.Entity(key=datastore_client.key(kind, name))
    entity.update({
    'Name/ID': 'name=num-visits',
    'count': val + 1
    })
    datastore_client.put(entity)



@app.route('/')
def home():

    msg = """
            Cloud Run API
            route /fetch
            
            """
    return msg

@app.route('/fetch')
def get_visits():
    val = get_counts()
    update_db()
    response = jsonify({'count': val})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    


    
    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))