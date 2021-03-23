import asyncio
import socket
import threading
import logging
import traceback
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9900))

while True:
    client.send(input(":::").encode("utf-8"))
    data = client.recv(4096)
    print(data.decode("utf-8"))