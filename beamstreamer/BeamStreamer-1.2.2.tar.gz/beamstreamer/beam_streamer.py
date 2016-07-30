"""Watch Beam streams in VLC."""

import requests
import xmltodict

import subprocess


class BeamStreamer(object):
    """Watch Beam streams in VLC."""

    def __init__(self):
        self.session = requests.Session()

    def open_stream(self, stream, quality="source"):
        data = self.session.get("https://beam.pro/api/v1/channels/{}?fields=id".format(stream)).json()
        user_id = data["id"]

        data = self.session.get("https://beam.pro/api/v1/channels/{}/manifest.smil".format(user_id)).text
        data = xmltodict.parse(data)

        sources = data["smil"]["body"]["switch"]["video"]
        if not isinstance(sources, list):
          	sources = [sources]

        streams = {(option["@title"] if not option["@title"].startswith("source") else "source"): option["@src"] for option in sources}

        if quality in streams:
            print("Loading stream...")

            source = data["smil"]["head"]["meta"]["@base"] + streams[quality]

            subprocess.call(["vlc", source])
        else:
            print("Quality not found.")
            print("Available:")

            for stream in streams:
                print(stream)

if __name__ == "__main__":
    bs = BeamStreamer()
    bs.open_stream("Monstercat", "source")
