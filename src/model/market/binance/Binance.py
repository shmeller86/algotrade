from src.model.market.binance.Engine import Engine
# from src.model.ws.WsClient import WsClient
from src.model.ws.WsServer import WsServer
import src.model.ws.ApiServer as ApiServer
from src.model.Base import Base
import logging
import threading
import traceback
import os
import json
import time
from pprint import pprint


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

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("algotrade.Binance")
        self.__backtest = kwargs['run_args']['backtest']
        self.__interval = kwargs['run_args']['interval']
        self.__limit = kwargs['run_args']['limit']
        self.__pairs = kwargs['run_args']['pairs']
        self.__ws_server = int(os.getenv('WS_START'))
        self.__api_server = int(os.getenv('API_START'))

    def start(self):
        # Run thread the websocket server for aggregation outside data.
        if self.__ws_server:
            wss = WsServer()
            thread_ws = threading.Thread(target=wss.run)
            thread_ws.start()

        # Run thread the API server for response inside data.
        if self.__api_server:
            thread_api = threading.Thread(target=ApiServer.run)
            thread_api.start()



        while True:
            pprint(wss.line)
            time.sleep(2)



        eng = Engine(self.run_args)
        #
        # # eng.get_candle()
        obj = eng.get_order_book()
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
