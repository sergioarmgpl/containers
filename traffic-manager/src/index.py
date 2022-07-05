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

ttl = os.environ["TTL"]

def redisCon():
   rhost = os.environ['REDIS_HOST']
   rauth = os.environ['REDIS_AUTH']
   return redis.StrictRedis(host=rhost,\
          port=6379,db=0,password=rauth,\
          decode_responses=True)

@app.route("/traffic", methods=["POST"])
def setTrafficObject():
    r = redisCon()
    data = request.json
    pos = data["position"]
    object_name = pos["object"]+"-"+str(int(time.time()))
    r.geoadd(f"traffic",[float(pos["lng"]),float(pos["lat"]),\
    object_name],ch=True)
    r.hset(f"object:{object_name}:data","type",pos["object"])
    r.hset(f"object:{object_name}:data","warning",pos["warning"])
    r.expire(f"object:{object_name}:data",ttl)
    return jsonify({"setTrafficObject":"done"})

@app.route("/traffic/objects/unit/<unit>/r/<radius>/lat/<lat>/lng/<lng>", methods=["GET"])
def getTrafficObjects(unit,radius,lat,lng):
    r = redisCon()

    objects = r.geosearch("traffic",unit=unit,radius=float(radius),
    longitude = lng,latitude=lat,sort="ASC")
    data = []
    for obj in objects:
        pos = r.geopos("traffic",obj)
        get warning and type metadata
        data.append({"object":obj,"lat":pos[0][0],"lng":pos[0][1]})    

    return jsonify({"getTrafficObjects":"done",
    "objects":data
    })

@app.route("/collector", methods=["GET"])
def clean(unit,radius,lat,lng):
    r = redisCon()

    objects = r.geosearch("traffic",unit=unit,radius=float(radius),
    longitude = lng,latitude=lat,sort="ASC")
    data = []
    for obj in objects:
        pos = r.geopos("traffic",obj)
        data.append({"object":obj,"lat":pos[0][0],"lng":pos[0][1]})    


    get keys zrange
    not exits key delete from set

    return jsonify({"getTrafficObjects":"done",
    "objects":data
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
