import json

import requests

from versiontracker.baseseekers import BaseSeeker


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.package = data.get('package', data['id'])

    def data(self):
        response = requests.get("https://pypi.python.org/pypi/{}/json".format(
            self.package))
        data = json.loads(response.text)
        version = data["info"]["version"]
        return {
            "id": self.id,
            "version": version,
            "date": data["releases"][version][0]["upload_time"],
            "url": data["info"]["release_url"],
        }
