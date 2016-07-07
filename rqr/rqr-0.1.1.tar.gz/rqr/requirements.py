import pip
import yaml

from .updater import get_last_version

FILENAME = 'rqr.yaml'


class Requirements:
    def __init__(self):
        self.pkgs = {}
        self.reload()

    def reload(self):
        try:
            with open(FILENAME, 'r') as stream:
                self.pkgs = yaml.load(stream)
                stream.close()
        except FileNotFoundError:
            self.pkgs = {}

    def add(self, pkg, target, version):
        if target not in self.pkgs:
            self.pkgs[target] = {}
        self.pkgs[target][pkg] = version
        self.save()

    def save(self):
        with open(FILENAME, 'w') as stream:
            yaml.dump(self.pkgs, stream, default_flow_style=False)
            stream.close()

    def install(self, pkg, target):
        version = str(get_last_version(pkg))
        if target:
            self.add(pkg, target, version)
        pip.main(['install', pkg])
        return { pkg: version }

    def __str__(self):
        res = []
        for target in self.pkgs:
            res.append(target + ':')
            for requirement in self.pkgs[target]:
                version = self.pkgs[target][requirement]
                res.append('  - {0}@{1}'.format(requirement, version))
        return '\n'.join(res)
