import os
import requests
import sys
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import json
from datetime import datetime
from geopy import distance

queue = []
traffic_events = []

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
   ts = str(int(datetime.timestamp(datetime.now())))
   event = {'lat': coor["lat"],
         'lng':coor["lng"],
         'ts':ts,
         'object':data["object"],
         'warning':data["warning"]}
   print(event,file=sys.stderr)
   traffic_events.append(event)
   return jsonify({"client_id":data["object"]+"-"+ts,"registerTrafficEvent":"done"})

@app.route("/traffic", methods=["GET"])
def syncTrafficEvents():
   global traffic_events
   headers={"Content-Type":"application/json"}
   print(traffic_events,file=sys.stderr)
   tf_tmp = traffic_events
   while len(tf_tmp) > 0:
      for i in range(0,len(tf_tmp)):
         if i+1 <= len(tf_tmp):
            for j in range(i+1,len(tf_tmp)):
               m = distance.distance(
                  (tf_tmp[i]["lat"],tf_tmp[i]["lng"]),
                  (tf_tmp[i]["lat"],tf_tmp[i]["lng"]),
               ).m
               if m < 5:
                  del tf_tmp[j]
   print("Filtered",tf_tmp,file=sys.stderr)
   r = requests.post(os.environ['ENDPOINT']
   + f"/traffic/1",json=
   {
      "data":tf_tmp
   })
   traffic_events.clear()
   return jsonify({"syncTrafficEvents":"done"})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=3000, debug=True)
