import requests

class Fec:

    def __init__(self, key):
        self.API_KEY = key

    def get(self, url, params="", pages=[1]):
        base = "https://api.open.fec.gov/v1"
        ret = {}
        for p in pages:
            req_url = base + url + "?api_key=" + self.API_KEY \
                      + "&page=" + str(p) + params
            r = requests.get(req_url)

            ret[p] = r.json()
        return ret

