import asyncio
import socket
from websocket import create_connection
import threading
import logging
import traceback
import os

# Connect to WebSocket API and subscribe to trade feed for XBT/USD and XRP/USD
ws = create_connection("wss://fstream.binance.com/ws/uniusdt@depth5@500ms")
# ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')

# Infinite loop waiting for WebSocket data
while True:
    print(ws.recv())

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.settimeout(2)
# client.connect(("fstream.binance.com", 443))
# # client.sendall(b"GET /ws/uniusdt@depth5@500ms HTTP/1.1\r\n\r\n")
# client.sendall(b"/ws/uniusdt@depth5@500ms")
# # s.connect(("fstream.binance.com", 9443))
# #             s.sendall(b"GET /ws/uniusdt@depth5@500ms HTTP/1.1\r\n\r\n")
# while True:
#
#     # client.send(input(":::").encode("utf-8"))
#     data = client.recv(4096)
#     if not data:
#         break
#     print(data.decode("utf-8"))