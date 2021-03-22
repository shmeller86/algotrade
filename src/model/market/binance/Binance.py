from src.model.market.binance.Engine import Engine
from src.model.ws.WsClient import WsClient
from src.model.Base import Base
import os
from pprint import pprint


class Binance(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super().__init__(arg, run_args=None)
        # self.run_args = run_args
        # pprint()
        self.start()

    def start(self):
        eng = Engine(self.run_args)


        # eng.get_candle()
        obj = eng.get_order_book()
        pprint(str(obj))
        ws = WsClient(url='ws://%s:%s' % (os.getenv('WS_DEST_HOST'), os.getenv('WS_DEST_PORT')))
        # ws.connect()
        # ws.run()
        # ws.start()
        # ws.send(str(obj))
        print(ws.is_connected())

        # self.get_candle()
        # self.get_open_interest()
        # self.get_top_trader_ratio()

