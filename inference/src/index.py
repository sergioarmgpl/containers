from flask import Flask, request
from flask import jsonify
import json
import sys

app = Flask(__name__)

from joblib import load
from sklearn import tree

import os
 
clf = None 

def loadModel():
    global clf
    model = "safety_rules.model"
    clf = load(model)
    print("model loaded",file=sys.stderr)

@app.route('/')
def hello():
    return "hello :)"

@app.route('/predict', methods=["POST"])
def predict():
    global clf
    data = json.loads(json.dumps(request.get_json()))
    data = { "prediction": clf.predict([data["data"]])[0] }
    return jsonify(data),200,{'Content-Type': 'application/json'}

@app.route('/_health')
def _health():
    return "_health"

if __name__ == '__main__':
    loadModel()
    app.run(host='0.0.0.0', port=3000, debug=True)