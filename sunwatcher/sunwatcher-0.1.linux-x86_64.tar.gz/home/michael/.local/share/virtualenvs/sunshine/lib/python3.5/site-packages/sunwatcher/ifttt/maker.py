# coding: utf-8

MAKER_ENDPOINT = "https://maker.ifttt.com/trigger/%s/with/key/%s"

import requests

class Maker(object):
    def __init__(self, key):
        self.key = key

    def trigger(self, event, values = []):
        if len(values) > 3:
            raise ValueError("Can only supply up to 3 values")

        data = {}

        if len(values) >= 1:
           data['value1'] = values[0]

        if len(values) >= 2:
            data['value2'] = values[1]

        if len(values) >= 3:
            data['value3'] = values[2]

        url = MAKER_ENDPOINT % (event, self.key)
        r = requests.post(url, json = data)

        return r.status_code == 200
