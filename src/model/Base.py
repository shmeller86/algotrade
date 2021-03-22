import os
import requests
import logging
import logging.config

run_args = None


class Base:
    """docstring for Base"""

    def __init__(self, run_args=None):
        if run_args is None:
            run_args = {}
        else:
            self.run_args = run_args

    def r_get(self, url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                return req.json()
        except Exception as e:
            print("Error get request = " + str(e))
            os._exit(0)

    def r_post(self):
        pass


class Logging:

    def __init__(self):
        config = {
            "version": 1,
            "handlers": {
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "full",
                    "filename": "log/info.log"
                },
            },
            "loggers": {
                "algotrade": {
                    "handlers": ["fileHandler"],
                    "level": os.getenv("LOGGING_LEVEL"),
                }
            },
            "formatters": {
                "classic": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                },
                "full": {
                    "format": "[%(asctime)s][%(processName)s][%(threadName)s][%(filename)s][%(funcName)s][%(levelname)s] - %(message)s"
                }
            }
        }

        logging.config.dictConfig(config)
        # logger = logging.getLogger("algotrade")
        # logger.setLevel(logging.INFO)
        # fh = logging.FileHandler("log/info.log")
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # fh.setFormatter(formatter)
        #
        # logger.addHandler(fh)



        # logging.basicConfig(filename="log/debug.log", level=logging.DEBUG)
        # logging.basicConfig(filename="log/info.log", level=logging.INFO)
        # logging.basicConfig(filename="log/error.log", level=logging.ERROR)
