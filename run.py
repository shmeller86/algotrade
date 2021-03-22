from dotenv import load_dotenv
from argparse import ArgumentParser
from src.model.market.binance.Binance import Binance
from src.model.ws.RunServer import *

load_dotenv()

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
parser.set_defaults(threads=1)
args = parser.parse_args()

if args.pairs:
    args.pairs = args.pairs.split(',')

if args.markets:
    args.markets = args.markets.split(',')

# run server the ws and the api
if args.server:
    run_server()
else:
    for market in args.markets:
        core[market](run_args=vars(args))
