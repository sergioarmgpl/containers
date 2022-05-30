from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import os
import redis




app = Flask(__name__)
CORS(app,origins=["*"])

uri = os.environ['MONGO_URI']
database = os.environ['MONGO_DB']

client = MongoClient(self.uri,retrywrites=False,maxPoolSize=None)
db = client[database]
collection = db["geodb"]
collection.find_one(query)

collection.insert_one(data)
self.collection.find(query)  



@app.route("/client/<cid>/position", methods=["POST"])
def setPosition(cid):
    data = request.json
    collection.insert_one({"cid":cid,"lat":lat,"lng":lng})

    return jsonify({"client_id":cid,"positionStored":"done"})


@app.route("/clients/positions/f/25-3-12/t/25-3-12", methods=["GET"])
def getPositions():
    data = []
    for key in r.scan_iter("client:*"):
        data.append({
            "cid":int(r.hget(key,"cid")),
            "lat":float(r.hget(key,"lat")),
            "lng":float(r.hget(key,"lng"))
        })
    return jsonify({"clients":data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
