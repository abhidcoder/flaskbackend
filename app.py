from flask import Flask,jsonify,request
import requests
import json
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=['http://localhost:3000'])

#Dependencies Notes
#pip install pymongo
#pip install flask_cors
#pip install dnspython

client = MongoClient('mongodb+srv://Firedrakesin:Garubb66@cluster0.iodwiy3.mongodb.net/')
db = client['Book-Store']
collection = db['Book_data']


@app.route("/", methods=['POST', 'GET'])
def home():
    json_values=[]
    documents = collection.find({}, {'_id': 0})
    for document in documents:
        json_values.append(document)

    payload = jsonify(json_values)
    return payload


@app.route("/lang/<lang>", methods=['POST', 'GET'])
def lang(lang):
    json_values_english=[]
    json_values_arabic=[]
    json_values_French=[]
    json_values_mixed=[]
    documents = collection.find({}, {'_id': 0})
    for document in documents:
      json_values_mixed.append(document)
      if document["language"]=="English":
        json_values_english.append(document)
      elif document["language"]=="Arabic":
        json_values_arabic.append(document)
      elif document["language"]=='French':
        json_values_French.append(document)

    if lang=="English": 
        return jsonify(json_values_english)
    if lang=="Arabic": 
      return jsonify(json_values_arabic)
    if lang=="French": 
      return jsonify(json_values_French)

    return jsonify(json_values_mixed)


@app.route("/price/<value>", methods=['POST', 'GET'])
def price_filter(value):
    json_values_lh = []
    json_values_hl = []
    json_values_mixed = []

    documents = list(collection.find({}, {'_id': 0}))

    json_values_lh = sorted(documents, key=lambda x: int(x["price"]))
    json_values_hl = sorted(documents, key=lambda x: int(x["price"]), reverse=True)
    json_values_mixed.append(documents)

    if value == "lh":
        return jsonify(json_values_lh)
    if value == "hl":
        return jsonify(json_values_hl)

    return jsonify(json_values_mixed[0])


@app.route('/store_data', methods=['POST'])
def store_data():
    data = request.get_json() 
    collection = db['book_json']
    collection.insert_one(data)
    return jsonify({"Message":"Data stored successfully"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)



# @app.route("/cc/<types>", methods=['POST', 'GET'])
# def client_specific_custom_pdf(types):
#     documents = collection.find()

#     headers = {
#         'Content-Type': 'application/json'
#     }

#     payload = json.dumps({"id": ""})
#     response = requests.request("POST", url, data=payload, headers=headers)
#     return response.text



