from flask import Response, Flask, request, jsonify
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge
import time
import redis
import os
import sys
import json

app = Flask(__name__)
t = Gauge('weather_metric1', 'temperature')
h = Gauge('weather_metric2', 'humidity')

rhost = os.environ['REDIS_HOST']
rauth = os.environ['REDIS_AUTH']
stopic = os.environ['SENSOR_TOPIC']
r = redis.StrictRedis(host=rhost,\
        port=6379,db=0,password=rauth,\
        decode_responses=True)

@app.route("/metrics")
def metrics():
    data = r.lpop(stopic)
    values = json.loads(str(data).replace("\'","\""))
    t.set(int(values["temperature"]))
    h.set(int(values["humidity"]))
    res = []
    res.append(prometheus_client.generate_latest(t))
    res.append(prometheus_client.generate_latest(h))
    print({"processed":true},file=sys.stderr)
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
