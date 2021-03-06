from dotenv import load_dotenv
from argparse import ArgumentParser
from src.model.market.binance.Binance import Binance
from src.model.ws.RunServer import *
from src.model.Base import Logging
import logging
import traceback

load_dotenv()
Logging()
logger = logging.getLogger("algotrade.initial")

logger.info("============= START APPLICATION =============")

core = {
    "bnc": Binance,
}
parser = ArgumentParser()
parser.add_argument("-m", "--markets", dest="markets", help="markets", default=[])
parser.add_argument("-p", "--pairs", dest="pairs", help="pairs", default=[])
parser.add_argument("-i", "--interval", dest="interval", help="interval", default='1h')
parser.add_argument("-s", "--server", dest="server", help="server", default=False)
parser.add_argument("-l", "--limit", dest="limit", help="limit", default='30')
parser.add_argument("-t", "--test", dest="backtest", help="backtest")
args = parser.parse_args()

if args.pairs:
    args.pairs = args.pairs.split(',')

if args.markets:
    args.markets = args.markets.split(',')

try:
    for market in args.markets:
        logger.info(f"Run the '{market}' market")
        core[market](run_args=vars(args)).start()
except Exception as e:
    logger.error("Uncaught exception: %s. \n %s", traceback.format_exc(), e)
# run server the ws and the api
# try:
#     if args.server:
#         run_server()
#         logger.debug("Wait 2 sec...")
#         time.sleep(2)
#         logger.debug("Servers is run!")
#         for market in args.markets:
#             core[market](run_args=vars(args))
#     else:
#         for market in args.markets:
#             core[market](run_args=vars(args))
# except:
#     logger.error("uncaught exception: %s", traceback.format_exc())

