from src.model.market.binance.Engine import Engine
from src.model.ws.WsServer import WsServer
from src.model.ws.WsClient import WsClent
import src.model.ws.ApiServer as ApiServer
from src.model.Base import Base
import logging
import threading
import asyncio
import traceback
import os
import json
import time
from pprint import pprint
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Binance:
    logger = None

    # Will use saved data for testing
    __backtest = None

    # Timeframe
    __interval = None

    # Limit Candles
    __limit = None

    # Market name
    __markets = 'bnc'

    # Pairs for analyse
    __pairs = None

    # Run websocket server
    __server = None

    __wss = None
    __bar = ''

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("algotrade.Binance")
        self.__backtest = kwargs['run_args']['backtest']
        self.__interval = kwargs['run_args']['interval']
        self.__limit = kwargs['run_args']['limit']
        self.__pairs = kwargs['run_args']['pairs']
        self.__ws_server = int(os.getenv('WS_START'))
        self.__api_server = int(os.getenv('API_START'))

    def run_buildbarchart(self):
        time.sleep(3)
        fig = plt.figure()
        animator = ani.FuncAnimation(fig, self.buildmebarchart, interval=100)
        plt.show()

    def buildmebarchart(self, i=int):
        # print(self.__wss.line['depth'][''])
        # prices = ['Nuclear', 'Hydro', 'Gas', 'Oil', 'Coal', 'Biofuel']
        # energy = []

        prices_a = [x for x in self.__wss.line['depth']['UNIUSDT']['a'].keys()]
        prices_b = [x for x in self.__wss.line['depth']['UNIUSDT']['b'].keys()]
        prices = prices_a[:20] + prices_b[:20]
        green = ['green'] * 20
        red = ['red'] * 20
        colors = green + red

        energy_a = [self.__wss.line['depth']['UNIUSDT']['a'][x] for x in self.__wss.line['depth']['UNIUSDT']['a']]
        energy_b = [self.__wss.line['depth']['UNIUSDT']['b'][x] for x in self.__wss.line['depth']['UNIUSDT']['b']]
        energy = energy_a[:20] + energy_b[:20]

        x_pos = [i for i, _ in enumerate(prices)]

        # while True:
        #     energy.append(random.randint(1, 1000))
        #     if len(energy) == 6:
        #         break
        plt.clf()
        plt.barh(x_pos, energy, color=colors, xerr=None)
        plt.ylabel("Price")
        plt.xlabel("Lots")
        plt.title("Order book for UNIUSDT")
        plt.yticks(x_pos, prices)

    def start(self):
        # Run thread the websocket server for aggregation outside data.
        if self.__ws_server:
            self.__wss = WsServer()
            thread_ws = threading.Thread(target=self.__wss.run)
            thread_ws.start()

        # Run thread the API server for response inside data.
        if self.__api_server:
            thread_api = threading.Thread(target=ApiServer.run)
            thread_api.start()

        # Run thread the socket client for communication.
        wsc = WsClent()
        thread_wc = threading.Thread(target=wsc.run)
        thread_wc.start()

        bnc = Engine(pairs=self.__pairs, limit=self.__limit, interval=self.__interval, test=self.__backtest, wsc=wsc)
        thread_bncwss_ob = threading.Thread(target=bnc.ws_order_book)
        thread_bncwss_ob.start()

        # Global request for order book to API binance
        threading.Thread(target=bnc.get_order_book).start()

        # Create the window with order book
        threading.Thread(target=self.run_buildbarchart).start()

        # while True:
        #     if 'depth' in self.__wss.line:
        #         energy_a = [self.__wss.line['depth']['UNIUSDT']['a'][x] for x in self.__wss.line['depth']['UNIUSDT']['a']]
        #         energy_b = [self.__wss.line['depth']['UNIUSDT']['b'][x] for x in self.__wss.line['depth']['UNIUSDT']['b']]
        #         energy = energy_a[:5] + energy_b[:5]
        #         print(energy)
        #
        #         prices_a = [x for x in self.__wss.line['depth']['UNIUSDT']['a'].keys()]
        #         prices_b = [x for x in self.__wss.line['depth']['UNIUSDT']['b'].keys()]
        #         prices = prices_a[:5] + prices_b[:5]
        #         print(prices)
        #         print(self.__wss.line['depth']['UNIUSDT'])
        #         print(self.__wss.line['depth']['UNIUSDT']['sum_ask'])
        #         print(self.__wss.line['depth']['UNIUSDT']['sum_bid'])
        #     # wsc.send(data='[{"type": "depth", "payload": {"pair": "UNIUSDT", "tx": "get", "data": {"a": [["1", "2"],["3", "5"]], "b": [["1", "2"]]}}}]')
        #     time.sleep(1)


        # bnc = Engine(pairs=self.__pairs, limit=self.__limit, interval=self.__interval,test=self.__backtest, wsc=wsc)
        # obj = bnc.get_order_book()
        # print(obj)

        #
        # ws = WsClient(url='ws://%s:%s' % (os.getenv('WS_DEST_HOST'), os.getenv('WS_DEST_PORT')))
        # # ws.connect()
        # threading.Thread(target=ws.connect()).start()
        # # ws.start()
        # # ws.send(str(obj))
        # print(ws.is_connected())
        # print("-------------------------------------")
        # self.get_candle()
        # self.get_open_interest()
        # self.get_top_trader_ratio()
