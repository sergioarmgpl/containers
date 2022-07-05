from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import requests
import os
import redis
import json
import sys
import time
  

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
    autoexpire()
