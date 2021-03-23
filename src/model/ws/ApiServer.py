import time
import json
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import logging

logger = logging.getLogger("algotrade.ApiServer")
line = {}
ws_message = {}
app = Flask(__name__)
CORS(app)


@app.route('/depth')
def api_line():
    global line

    if request.args.get('pair'):
        try:
            resp = line['depth'][request.args.get('pair')]
        except KeyError:
            resp = {}
    else:
        resp = line

    return jsonify(resp)


def run():
    logger.info("Run API SERVER.")
    app.run(host=os.getenv("API_HOST"),
            port=os.getenv("API_PORT"),
            debug=False,
            use_reloader=False)
