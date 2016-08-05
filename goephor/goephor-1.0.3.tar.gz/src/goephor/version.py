import json
import os

def string():
    path = os.path.dirname(os.path.abspath(__file__))
    version_path = "%s/%s" % (path,'version.json')
    with open(version_path) as version_file:
        version = json.load(version_file)
        return version.get('version')