import websocket
import threading
import json


class WsClient(threading.Thread):
    def __init__(self, url=None, on_open=None, on_message=None, on_error=None, on_close=None):
        super().__init__()

        self._is_stopped = False
        self._is_connected = False

        self._ws = None
        self._ws_url = url
        self.on_open_cb = on_open
        self.on_message_cb = on_message
        self.on_close_cb = on_close
        self.on_error_cb = on_error

        self._ws = websocket.WebSocketApp(
            url=self._ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

    def run(self):
        self.connect()
        # threading.Thread(target=self.connect())

    def connect(self):
        self._is_stopped = False
        self._ws.run_forever(sslopt={"check_hostname": False})

    def stop(self):
        self._is_stopped = True
        if self._is_connected:
            self._ws.close()

    def close(self):
        if self._is_connected:
            self._ws.close()

    def send(self, data):
        data = data if isinstance(data, str) else json.dumps(data)
        self._ws.send(data)

    def on_message(self, msg):
        if self.on_message_cb:
            self.on_message_cb(msg)

    def on_error(self, error):
        print(error)
        if self.on_error_cb:
            self.on_error_cb()

    def on_close(self):
        print("### websocket closed ###")
        self._is_connected = False
        if self.on_close_cb:
            self.on_close_cb()

    def on_open(self):
        print("### websocket connected ###")
        self._is_connected = True

        if self.on_open_cb:
            self.on_open_cb()

    def is_connected(self):
        return self._is_connected
