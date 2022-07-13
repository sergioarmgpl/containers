from flask import Flask,request,redirect,Response
import os
import requests
app = Flask(__name__)
url = os.environ['URL']

@app.route('/<path:path>',methods=['GET'])
def proxy(path):
   global url
   r = requests.get(f'{url}/{path}')
   excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
   headers = [(name, value) for (name, value) in  r.raw.headers.items() if name.lower() not in excluded_headers]
   response = Response(r.content, r.status_code, headers)
   return response

if __name__ == '__main__':
   app.run(debug = False,port=5000)