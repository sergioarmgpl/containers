from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import requests
import os
import redis
import json
import sys
import time
  
app = Flask(__name__)
CORS(app,origins=["*"])

ttl_trf = int(os.environ["TTL_TRAFFIC"])
ttl_obj = int(os.environ["TTL_OBJECT"])

def redisCon():
   rhost = os.environ['REDIS_HOST']
   rauth = os.environ['REDIS_AUTH']
   return redis.StrictRedis(host=rhost,\
          port=6379,db=0,password=rauth,\
          decode_responses=True)

@app.route("/traffic/1", methods=["POST"])
def setBulkTrafficObjects():
    global ttl_trf,ttl_obj
    r = redisCon()
    data = request.json
    warnings = data["data"]
    for w in warnings:
        object_name = w["object"]+"-"+w["ts"]

        similar = r.geosearch("traffic",unit="m",radius=5.0,
        longitude = float(w["lng"]),latitude=float(w["lat"]),sort="ASC")
        print("similar",similar,file=sys.stderr)

        n_similar = 0
        for s_obj in similar:
            o_type = r.hget(f"object:{s_obj}:data","type")
            print(o_type,w["object"],o_type == w["object"],file=sys.stderr)
            if o_type == w["object"]:
                n_similar += 1
                print("found similar",file=sys.stderr)
        
        if n_similar == 0:
            r.geoadd(f"traffic",[float(w["lng"]),float(w["lat"]),\
            object_name],ch=True)
            r.hset(f"object:{object_name}:data","type",w["object"])
            r.hset(f"object:{object_name}:data","warning",w["warning"])
            r.expire("traffic",ttl_trf)
            r.expire(f"object:{object_name}:data",ttl_obj)
            print({"inserting":object_name},file=sys.stderr)
        else:
            print({"found":"similar GPS coordinates"},file=sys.stderr)
    return jsonify({"setTrafficObject":"done"})

@app.route("/traffic/2", methods=["POST"])
def setSingleTrafficObject():
    global ttl_trf,ttl_obj
    r = redisCon()
    data = request.json
    pos = data["position"]
    object_name = w["object"]+"-"+w["ts"]
    r.geoadd(f"traffic",[float(pos["lng"]),float(pos["lat"]),\
    object_name],ch=True)
    r.hset(f"object:{object_name}:data","type",data["object"])
    r.hset(f"object:{object_name}:data","warning",data["warning"])
    r.hset(f"object:{object_name}:data","ts",data["ts"])
    r.expire("traffic",ttl_trf)
    r.expire(f"object:{object_name}:data",ttl_obj)
    return jsonify({"setTrafficObject":"done"})

@app.route("/traffic/unit/<unit>/r/<radius>/lat/<lat>/lng/<lng>", methods=["GET"])
def getTrafficObjects(unit,radius,lat,lng):
    r = redisCon()

    objects = r.geosearch("traffic",unit=unit,radius=float(radius),
    longitude = lng,latitude=lat,sort="ASC")
    data = []
    for obj in objects:
        pos = r.geopos("traffic",obj)
        #get warning and type metadata
        obj_data = r.hgetall(f"object:{obj}:data")
        print(obj_data,file=sys.stderr)
        data.append({
        "object":obj,
        "lat":pos[0][1],
        "lng":pos[0][0],
        "type":obj_data["type"],
        "warning":obj_data["warning"]
        })    

    return jsonify({"getTrafficObjects":"done",
    "objects":data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
