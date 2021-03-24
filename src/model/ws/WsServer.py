import logging
import json
import pprint
import traceback
import asyncio
import socket
from json import JSONDecodeError
import os

from src.model.ws.SocketBase import SocketBase


class WsServer(SocketBase):

    def __init__(self):
        super(WsServer, self).__init__()
        self.server_sock.bind((os.getenv("WS_HOST"), int(os.getenv("WS_PORT"))))
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.listen()

        self.line = {}
        self.logger = logging.getLogger("algotrade.WsServer")

    async def main(self):
        await self.main_loop.create_task(self.accept_socket())

    async def accept_socket(self):
        while True:
            client_sock, addr = await self.main_loop.sock_accept(self.server_sock)
            if addr:
                self.logger.info(f"connection from {addr}")
            self.main_loop.create_task(self.listen_socket(client_sock, addr))

    async def listen_socket(self, client_sock=None, addr=None):
        if not client_sock or not addr:
            return

        while True:
            request = await self.main_loop.sock_recv(client_sock, 4096)
            self.logger.debug(f"Receive from {addr} : {request}")

            try:
                obj = json.loads(request.decode('utf-8').replace('\n', ''))
            except JSONDecodeError as e:
                await self.send_data(client_sock, 'BAD_REQUEST\n')
                self.logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)
            except Exception as e:
                self.logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)
            else:
                await self.parse_receive_message(obj)
                await self.send_data(client_sock, 'OK\n')

    async def send_data(self, client_sock=None, data=None):
        response = data.encode()
        await self.main_loop.sock_sendall(client_sock, response)

    async def parse_receive_message(self, message):
        # [{"type": "depth", "payload": {"pair": "UNIUSDT", "tx": "get", "data": {"a": [["1", "2"]], "b": [["1", "2"]]}}}]
        # obj = {
        #     "type": "depth",
        #     "payload": {
        #         "pair": self.run_args['pairs'][0],
        #         "tx": "get",
        #         "data": {
        #             "a": self.candle['asks'],
        #             "b": self.candle['bids'],
        #         }
        #     }
        # }
        try:
            for item in message:
                # Глубина стакана.
                if item['type'] == 'depth':

                    # Если нет, то создаем.
                    if item['type'] not in self.line.keys():
                        self.line[item['type']] = {}

                    # Если нет пары, то создаем.
                    if item['payload']['pair'] not in self.line[item['type']].keys():
                        self.line[item['type']][item['payload']['pair']] = {"a": {}, "b": {}}

                    # Обновляем БИДы
                    for bid in item['payload']['data']['b']:
                        self.line[item['type']][item['payload']['pair']]['b'][bid[0]] = float(bid[1])
                    # Обновляем АСКи
                    for ask in item['payload']['data']['a']:
                        self.line[item['type']][item['payload']['pair']]['a'][ask[0]] = float(ask[1])

                    # Обновляем сумму АСКов
                    self.line[item['type']][item['payload']['pair']]['sum_ask'] = float(sum(
                        self.line[item['type']][item['payload']['pair']]['a'][x] for x in
                        self.line[item['type']][item['payload']['pair']]['a']))
                    # Обновляем сумму БИДов
                    self.line[item['type']][item['payload']['pair']]['sum_bid'] = float(sum(
                        self.line[item['type']][item['payload']['pair']]['b'][x] for x in
                        self.line[item['type']][item['payload']['pair']]['b']))
        except Exception as e:
            self.logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)




