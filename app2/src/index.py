from flask import Flask 
from flask import jsonify 
import os 
import socket 

app = Flask(__name__) 

host = socket.gethostname() 

msg = os.environ['MESSAGE'] 

@app.route('/')
def index(): 
    return jsonify({"host":host,"msg":msg}) 

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)
