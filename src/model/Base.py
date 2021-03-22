import os
import requests

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
