from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import requests
import os
import redis
import json
import sys

app = Flask(__name__)
CORS(app,origins=["*"])

def redisCon():
   rhost = os.environ['REDIS_HOST']
   rauth = os.environ['REDIS_AUTH']
   return redis.StrictRedis(host=rhost,\
          port=6379,db=0,password=rauth,\
          decode_responses=True)

@app.route("/client/<cid>/position", methods=["POST"])
def setPosition(cid):
    r = redisCon()
    data = request.json
    key = f"client:{cid}:position"
    r.hset(key,"cid",data["cid"])
    r.hset(key,"lat",data["lat"])
    r.hset(key,"lng",data["lng"])
    r.expire(key,180)

    data = {'lat': data["lat"],
            'lng':data["lng"],
            'cid':data["cid"]}
    headers={"Content-Type":"application/json"}
    r = requests.post(os.environ['ENDPOINT']
        + f"/client/{cid}/position",json=data)

    return jsonify({"client_id":cid,"setPosition":"done"})


@app.route("/clients/positions/unit/<unit>/r/<radius>", methods=["GET"])
def getPositions(unit,radius):
    r = redisCon()
    data = []
    for key in r.scan_iter("client:*:position"):
        lat = float(r.hget(key,"lat"))
        lng = float(r.hget(key,"lng"))
        cid = int(r.hget(key,"cid"))
        near = r.geosearch(f"client:{cid}:stops",unit=unit,radius=float(radius),
        longitude=lng,latitude=lat,sort="ASC")        
        data.append({
            "cid":cid,
            "lat":lat,
            "lng":lng,
            "near":near
        })
    return jsonify({"clients":data})

@app.route("/client/<cid>/stops", methods=["POST"])
def setStops(cid):
    r = redisCon()
    data = request.json
    stops = data["stops"]
    for stop in stops:
       r.geoadd(f"client:{cid}:stops",[float(stop["lng"]),float(stop["lat"]),stop["name"]],xx=True)
    r.expire(f"client:{cid}:stops",3600*10)
    return jsonify({"setStops":"done"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
