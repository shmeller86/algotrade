import socket
import asyncio
import os


class SocketBase:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_loop = asyncio.new_event_loop()
        # print(self.main_loop)

    async def main(self):
        raise NotImplementedError()

    async def listen_socket(self):
        raise NotImplementedError()

    async def accept_socket(self):
        raise NotImplementedError()

    async def send_data(self, client_sock=None, data=None):
        raise NotImplementedError()

    def run(self):
        self.main_loop.run_until_complete(self.main())
