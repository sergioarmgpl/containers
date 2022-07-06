from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app,origins=["*"])

@app.route("/")
def map():
   return render_template("traffic.html",GPS_SERVER=os.environ["GPS_SERVER"]
                         ,LATITUDE=os.environ["LATITUDE"]
                         ,LONGITUDE=os.environ["LONGITUDE"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
