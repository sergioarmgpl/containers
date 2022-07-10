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
   print("len_traffic",len(traffic_events),file=sys.stderr)
   tf_tmp = traffic_events
   for i in range(0,len(tf_tmp)):
       print("tf_tmp len",len(tf_tmp))
       if i+1 <= len(tf_tmp):
          for j in range(i+1,len(tf_tmp)):
             if tf_tmp[i] != None:
                print(f"tf_tmp[{i}]",tf_tmp[i])
                print(f"tf_tmp[{j}]",tf_tmp[j])
                print("----")
                m = distance.distance(
                (tf_tmp[i]["lat"],tf_tmp[i]["lng"]),
                (tf_tmp[j]["lat"],tf_tmp[j]["lng"]),
                ).meters
                print("m",m,file=sys.stderr)
                print(tf_tmp[i]["object"],tf_tmp[j]["object"],file=sys.stderr)
                if m < 5 and tf_tmp[i]["object"] == tf_tmp[j]["object"]:
                    tf_tmp[j]= None
                    print(f"Marked tf_tmp[{j}] to remove")
   k = 0
   while k <= len(tf_tmp)-1:
      if tf_tmp[k] == None:
         print("removed",tf_tmp[k])
         del tf_tmp[k]
      else:
         k += 1
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
