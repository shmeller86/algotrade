import pprint as p
import pandas as pd
from datetime import datetime
from src.model.Base import Base
import os
import logging
import traceback
import json
import socket
import time
from websocket import create_connection
import threading


class Engine:
    logger = None
    REQUEST_URL = {
        "F_KLINES": ["GET",
                     "https://fapi.binance.com/fapi/v1/klines?symbol=%s&limit=%s&interval=%s"],
        "OPEN_INTEREST_HITS": ["GET",
                               "https://www.binance.com/futures/data/openInterestHist?symbol=%s&limit=%s&period=%s"],
        "TOP_TRADER_RATIO": ["GET",
                             "https://www.binance.com/futures/data/topLongShortAccountRatio?symbol=%s&limit=%s&period=%s"],
        "ORDER_BOOK": ["GET",
                       "https://fapi.binance.com/fapi/v1/depth?symbol=%s&limit=%s"]
    }
    candle = None
    df = None
    debug = True
    b = None

    pairs = None
    interval = None
    limit = None
    test = None
    wsc = None

    def __init__(self, pairs=None, interval=None, limit=None, test=False, wsc=None):
        self.logger = logging.getLogger("algotrade.Binance")
        self.b = Base()
        self.pairs = pairs
        self.interval = interval
        self.limit = limit
        self.test = test
        self.wsc = wsc


    def get_top_trader_ratio(self):
        """
            Top Trader Long/Short Ratio (Accounts) (MARKET_DATA)
            Name        Type    Mandatory   Description
            symbol      STRING  YES
            period      ENUM    YES         "5m","15m","30m","1h","2h","4h","6h","12h","1d"
            limit       LONG    NO          default 30, max 500
            startTime   LONG    NO
            endTime     LONG    NO
        """
        self.candle = self.b.r_get(self.REQUEST_URL['TOP_TRADER_RATIO'][1] % (
            self.run_args['pairs'][0], self.run_args['limit'], self.run_args['interval']))

        d_ = []
        c_ = [
            'ttr_longShortRatio',  # long/short account num ratio of top traders
            'ttr_longAccount',  # long account num ratio of top traders
            'ttr_shortAccount',  # long account num ratio of top traders
            'index',  # timestamp
        ]

        for item in self.candle:
            d_.append([
                item['longShortRatio'],
                item['longAccount'],
                item['shortAccount'],
                item['timestamp'],
            ])

        df = pd.DataFrame(d_, columns=c_)
        self.df = pd.merge(left=self.df, right=df, on="index")

        if self.debug: p.pprint(self.df)

    def get_open_interest(self):
        """
            Получаем данные по открытому интересу
            Name        Type    Mandatory   Description
            symbol      STRING  YES
            period      ENUM    YES         "5m","15m","30m","1h","2h","4h","6h","12h","1d"
            limit       LONG    NO          default 30, max 500
            startTime   LONG    NO
            endTime     LONG    NO
        """
        self.candle = self.b.r_get(self.REQUEST_URL['OPEN_INTEREST_HITS'][1] % (
            self.run_args['pairs'][0], self.run_args['limit'], self.run_args['interval']))

        d_ = []
        c_ = [
            'i_toi',  # total open interest
            'i_toiv',  # total open interest value
            'i_s',  # symbol
            'index',  # timestamp
        ]

        for item in self.candle:
            d_.append([
                item['sumOpenInterest'],
                item['sumOpenInterestValue'],
                item['symbol'],
                item['timestamp'],
            ])

        df = pd.DataFrame(d_, columns=c_)
        self.df = pd.merge(left=self.df, right=df, on="index")

        if self.debug:
            p.pprint(self.df)

    def get_candle(self):
        """Получаем осноные данные по свечам"""
        self.candle = self.b.r_get(self.REQUEST_URL['F_KLINES'][1] % (self.run_args['pairs'][0], self.run_args['limit'], self.run_args['interval']))

        d_ = []
        c_ = [
            'index',  # Open timestamp
            'o_t',  # Open time
            'o',  # Open
            'h',  # High
            'l',  # Low
            'c',  # Close
            'v',  # Volume
            'c_t',  # Close time
            'qas',  # Quote asset volume
            'not',  # Number of trades
            'tbbav',  # Taker buy base asset volume
            'tbqav',  # Taker buy quote asset volume
            'i'  # Ignore
        ]

        for item in self.candle:
            d_.append([
                item[0],
                datetime.fromtimestamp(int(str(item[0])[:-3])),
                item[1],
                item[2],
                item[3],
                item[4],
                item[5],
                item[6],
                item[7],
                item[8],
                item[9],
                item[10],
                item[11]
            ])

        self.df = pd.DataFrame(d_, columns=c_)

        if self.debug:
            p.pprint(self.df)

    def get_order_book(self):
        """Получаем данные по отложкам в стакане
            Limit	        Weight
            5, 10, 20, 50	2
            100	            5
            500	            10
            1000	        20
        """
        try:
            time.sleep(5)
            self.candle = self.b.r_get(self.REQUEST_URL['ORDER_BOOK'][1] % (self.pairs[0], self.limit))

            obj = {
                "type": "depth",
                "payload": {
                    "pair": self.pairs[0],
                    "tx": "get",
                    "data": {
                        "a": self.candle['asks'],
                        "b": self.candle['bids'],
                    }
                }
            }
            self.logger.debug(str(obj))
        except Exception as e:
            self.logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)
            os._exit(0)
        finally:
            if self.wsc:
                self.wsc.send(data=str([obj]).replace("'", '"'))

    def ws_order_book(self):
        ws = create_connection("wss://fstream.binance.com/ws/uniusdt@depth20@100ms")

        while True:
            try:
                data = ws.recv()
                data = json.loads(data)
                # p.pprint(data)
                obj = {
                    "type": "depth",
                    "payload": {
                        "pair": self.pairs[0],
                        "tx": "wss",
                        "data": {
                            "a": data['a'],
                            "b": data['b'],
                        }
                    }
                }
                self.logger.debug(str(obj))
            except Exception as e:
                self.logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)
                os._exit(0)
            finally:
                if self.wsc:
                    self.wsc.send(data=str([obj]).replace("'", '"'))
