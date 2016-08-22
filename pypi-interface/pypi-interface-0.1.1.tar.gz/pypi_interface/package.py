import requests

class Package(object):
    info_url = "https://pypi.python.org/pypi/{}/json"

    def __init__(self, name):
        json = self.get_json(name)
        self.info = json["info"]
        self.releases = json["releases"]

    @classmethod
    def get_json(cls, name):
        response = requests.get(cls.info_url.format(name))
        return response.json()

    @property
    def latest(self):
        return self.info["version"]
