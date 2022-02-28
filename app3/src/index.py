from flask import Flask, request

from cloudevents.http import from_http

app = Flask(__name__)

@app.route("/", methods=["POST"])
def route():
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())
    app.logger.warning(event)

    #You can access the fields id,source,type and specversion
    #in the event array such as event['id']

    #You can also call a serverless function with their URL
    #see the client.py field for this

    return "", 204

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)
