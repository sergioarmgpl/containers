import os
import requests
import sys

from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import json
from datetime import datetime

queue = []
traffic_events = []
cid = "cid-"+str(int(datetime.timestamp(datetime.now())))

app = Flask(__name__)
CORS(app,origins=["*"])

@app.route("/traffic/event", methods=["POST"])
def registerTrafficEvent():
   global queue,traffic_events,cid
   f = open("/tmp/gps","r")
   raw = f.readline()
   coor = json.loads(raw)
   f.close()
   data = json.loads(request.data)
   event = {'lat': coor["lat"],
         'lng':coor["lng"],
         'object':data["object"],
         'warning':data["warning"]}
   print(event,file=sys.stderr)
   traffic_events.append(event)
   return jsonify({"client_id":cid,"registerTrafficEvent":"done"})

@app.route("/traffic", methods=["GET"])
def syncTrafficEvents():
   global traffic_events
   headers={"Content-Type":"application/json"}
   r = requests.post(os.environ['ENDPOINT']
   + f"/traffic",json=
   {
      "data":traffic_events
   })
   traffic_events.clear()
   return jsonify({"client_id":cid,"syncTrafficEvents":"done"})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=3000, debug=True)
