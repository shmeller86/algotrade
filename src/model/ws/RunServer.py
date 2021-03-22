from src.model.ws.WsServer import WsServer
import time
import json
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

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


def on_message(msg):
    global ws_message
    json_data = json.loads(msg)
    ws_message = json_data
    parse_ws_message(ws_message)
    print('-------------\n')


def on_disconnect():
    global line
    global ws_message

    print("Clearing line")
    line = {}
    ws_message = {}


def parse_ws_message(message):
    for item in message:

        # Глубина стакана.
        if item['type'] == 'depth':

            # Если нет, то создаем.
            if item['type'] not in line.keys():
                line[item['type']] = {}

            # Если нет пары, то создаем.
            if item['payload']['pair'] not in line[item['type']].keys():
                line[item['type']][item['payload']['pair']] = {"a": {}, "b": {}}

            # Обновляем БИДы
            for bid in item['payload']['data']['b']:
                line[item['type']][item['payload']['pair']]['b'][bid[0]] = float(bid[1])
            # Обновляем АСКи
            for ask in item['payload']['data']['a']:
                line[item['type']][item['payload']['pair']]['a'][ask[0]] = float(ask[1])

            # Обновляем сумму АСКов
            line[item['type']][item['payload']['pair']]['sum_ask'] = float(sum(line[item['type']][item['payload']['pair']]['a'][x] for x in line[item['type']][item['payload']['pair']]['a']))
            # Обновляем сумму БИДов
            line[item['type']][item['payload']['pair']]['sum_bid'] = float(sum(line[item['type']][item['payload']['pair']]['b'][x] for x in line[item['type']][item['payload']['pair']]['b']))


def run_server():
    ws_server = WsServer(
        host=os.getenv("WS_SERVER_HOST"),
        port=os.getenv("WS_SERVER_PORT"),
        on_message=on_message,
        on_disconnect=on_disconnect
    )

    ws_server.start()
    app.run(host=os.getenv("API_SERVER_HOST"), port=os.getenv("API_SERVER_PORT"))

    while True:
        time.sleep(0.1)
