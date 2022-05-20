from flask import Flask, request
from flask import jsonify
import os
import redis

app = Flask(__name__)
rhost = os.environ['REDIS_HOST']
rauth = os.environ['REDIS_AUTH']
r = redis.StrictRedis(host=rhost,\
        port=6379,db=0,password=rauth,\
        decode_responses=True)

@app.route("/client/<cid>/position", methods=["POST"])
def setPosition(cid):
    data = request.json
    key = f"client:{cid}:position"
    r.hset(key,"latitude",data["lat"])
    r.hset(key,"longitude",data["lng"])
    r.expire(key,180)
    return jsonify({"client_id":cid,"setPosition":"done"})

@app.route("/clients/positions", methods=["GET"])
def getPositions():
    return jsonify({"none":True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
