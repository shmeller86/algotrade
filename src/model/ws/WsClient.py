import asyncio
import socket
import threading
import logging
import traceback
import os
from src.model.ws.SocketBase import SocketBase


class WsClent(SocketBase):
    def __init__(self):
        super(WsClent, self).__init__()
        self.server_sock.connect((os.getenv("WS_HOST"), int(os.getenv("WS_PORT"))))
        self.server_sock.setblocking(False)
        self.logger = logging.getLogger("algotrade.WsClient")

    async def main(self):
        await self.main_loop.create_task(self.listen_socket())

    def accept_socket(self):
        pass

    async def listen_socket(self):
        while True:
            request = await self.main_loop.sock_recv(self.server_sock, 4096)
            self.logger.debug(f"Receive from WsServer: {request}")

    async def send_data(self, client_sock=None, data=None):
        if data:
            response = data.encode()
            await self.main_loop.sock_sendall(self.server_sock, response)

    def send(self, data=None):
        asyncio.run(self.send_data(data=data))
