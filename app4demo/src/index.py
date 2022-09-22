from flask import Flask, request, make_response
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def route():
    app.logger.warning(request.data)
    app.logger.warning(os.environ['MESSAGE'])

    response = make_response({
        "ENV_VAR": os.environ['MESSAGE']
    })
    response.headers["Ce-Id"] = str(uuid.uuid4())
    response.headers["Ce-specversion"] = "1.0"
    response.headers["Ce-Source"] = "test-sequence"
    response.headers["Ce-Type"] = "event.call.sequence"

    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)
