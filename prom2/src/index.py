from flask import Response, Flask, request, jsonify

import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge
import time

app = Flask(__name__)

_INF = float("inf")

g = Gauge('weather_metric', 'Temp')

@app.route("/temperature/<temp>", methods=["GET"])
def temperature(temp):
   g.set(int(temp))
   return jsonify({"msg":"Temperature received"})

@app.route("/metrics")
def requests_count():
    print(g)
    res = []
    res.append(prometheus_client.generate_latest(g))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
