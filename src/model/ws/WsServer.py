import asyncio
import websockets
import threading


class WsServer(threading.Thread):
    def __init__(self, host, port, on_message, on_disconnect):
        super().__init__()

        self._host = host
        self._port = port

        self._on_message = on_message
        self._on_disconnect = on_disconnect

        self._server = None
        self._connects = set()
        self._loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self._loop)

        start_server = websockets.server.serve(
            self.receive,
            self._host,
            self._port,
            ping_interval=120,
            ping_timeout=120,
            max_size=None
        )

        self._server = asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def get_loop(self):
        return self._loop

    def register(self, websocket):
        self._connects.add(websocket)
        print('registered')

    def unregister(self, websocket):
        try:
            self._connects.remove(websocket)
            self._on_disconnect()
            print('unregistered')
        except KeyError:
            pass

    def shutdown(self):
        print("[!] Shutdown ws server..")
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def receive(self, websocket, _):
        self.register(websocket)

        try:
            async for raw_msg in websocket:
                self._on_message(raw_msg)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.unregister(websocket)
