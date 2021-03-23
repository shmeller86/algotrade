import socket
import asyncio
import os


class SocketBase:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((os.getenv("WS_HOST"), int(os.getenv("WS_PORT"))))
        self.server_sock.setblocking(False)
        self.main_loop = asyncio.get_event_loop()

    async def main(self):
        raise NotImplementedError()

    async def listen_socket(self):
        raise NotImplementedError()

    async def accept_socket(self):
        raise NotImplementedError()

    async def send_data(self):
        raise NotImplementedError()

    def run(self):
        self.main_loop.run_until_complete(self.main())
