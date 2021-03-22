from src.model.market.binance.Engine import Engine
from src.model.ws.WsClient import WsClient
from src.model.Base import Base
import logging
import threading
import traceback
import os
from pprint import pprint




class Binance(Base):
    logger = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("algotrade.Binance")
        self.start()

    def start(self):
        eng = Engine(self.run_args)

        # eng.get_candle()
        obj = eng.get_order_book()

        ws = WsClient(url='ws://%s:%s' % (os.getenv('WS_DEST_HOST'), os.getenv('WS_DEST_PORT')))
        # ws.connect()
        threading.Thread(target=ws.connect()).start()
        # ws.start()
        # ws.send(str(obj))
        print(ws.is_connected())
        print("-------------------------------------")
        # self.get_candle()
        # self.get_open_interest()
        # self.get_top_trader_ratio()

