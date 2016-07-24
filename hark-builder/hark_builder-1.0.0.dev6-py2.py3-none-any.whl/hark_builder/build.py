import os
import json


def packer_file_path():
    return os.path.join(
        os.path.dirname(__file__),
        'packer', 'hark.json')


class Build(object):
    def __init__(self, name):
        self.name = name
        guest, driver = self.name.split('_')
        self.guest = guest
        self.driver = driver

    def __str__(self):
        return '%s - %s' % (self.guest, self.driver)

    @classmethod
    def all(cls):
        with open(packer_file_path(), 'r') as f:
            packer_conf = json.load(f)

        builds = []
        for build_conf in packer_conf['builders']:
            builds.append(cls(build_conf['name']))

        return builds

    @classmethod
    def by_name(cls, name):
        return cls(name)
