from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import os
import sys
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app,origins=["*"])

def mongoCon():
   uri = os.environ['MONGO_URI']
   database = os.environ['MONGO_DB']
   client = MongoClient(uri,retrywrites=False,maxPoolSize=None)
   db = client[database]
   collection = db["tracking"]
   return collection


@app.route("/client/<cid>/position", methods=["POST"])
def storePosition(cid):
    data = request.json
    dtnow = datetime.now()
    dtxt = str(dtnow).split(".")[0]
    ts = int(datetime.timestamp(dtnow))
    collection = mongoCon()
    collection.insert_one({
    "cid":data["cid"],"lat":data["lat"],"lng":data["lng"],
    "ts":ts,"dtxt":dtxt})
    return jsonify({"client_id":cid,"positionStored":"done"})

#dd-mm-yy-HH:MM:SS
@app.route("/client/<cid>/positions/s/<sdate>/e/<edate>",methods=["GET"])
def getPositions(cid,sdate,edate):
    st = datetime.strptime(sdate,"%d-%m-%y-%H:%M:%S")
    st = int(datetime.timestamp(st))
    et = datetime.strptime(edate,"%d-%m-%y-%H:%M:%S")
    et = int(datetime.timestamp(et))
    collection = mongoCon()
    cursor = collection.find({"cid":cid,"ts":{"$gte":st,"$lte":et}},{"_id":0})
    data = []
    for doc in cursor: 
       data.append(doc)
    print(data,file=sys.stderr)
    return jsonify({"tracking":data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
