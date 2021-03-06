from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return "Host:"+socket.gethostname()+os.environ['MESSAGE']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']), debug=True)
