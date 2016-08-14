# coding: utf-8

SOLARLOG_REQUEST_URL = 'getjp'
SOLARLOG_REQUEST_PAYLOAD = { 801: { 170: None } }

import requests

class Client(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.url = SOLARLOG_REQUEST_URL
        self.payload = SOLARLOG_REQUEST_PAYLOAD

    def get_data(self):
        url = "%s/%s" % (self.endpoint, self.url)
        r = requests.post(url, json = self.payload)

        if r.status_code == 200:
            return(self.parse_data(r.json()))
        else:
            return {}

    def parse_data(self, data):
        data = data['801']['170']

        out = {
            "time":                  data['100'],
            "power_ac":              data['101'],
            "power_dc":              data['102'],
            "voltage_ac":            data['103'],
            "voltage_dc":            data['104'],
            "yield_day":             data['105'],
            "yield_yesterday":       data['106'],
            "yield_month":           data['107'],
            "yield_year":            data['108'],
            "yield_total":           data['109'],
            "consumption_ac":        data['110'],
            "consumption_day":       data['111'],
            "consumption_yesterday": data['112'],
            "consumption_month":     data['113'],
            "consumption_year":      data['114'],
            "consumption_total":     data['115'],
            "total_power":           data['116']
        }

        return out
