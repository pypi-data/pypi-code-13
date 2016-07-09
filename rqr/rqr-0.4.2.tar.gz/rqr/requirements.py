import itertools
import pip
import yaml

from .updater import Updater
from .migrator import Migrator

FILENAME = 'rqr.yaml'


class Requirements:
    def __init__(self):
        self.pkgs = {}
        self.migrator = Migrator()
        self.updater = Updater()
        self.reload()

    def reload(self):
        try:
            with open(FILENAME, 'r') as stream:
                self.pkgs = yaml.load(stream)
                stream.close()
        except FileNotFoundError:
            self.pkgs = {}

    def migrate(self):
        # TODO: rather merge than override
        self.pkgs = self.migrator.run()
        self.save()

    def update(self, save = True):
        old_pkgs = self.pkgs
        self.pkgs, updates  = self.updater.update(self.pkgs)
        if save:
            self.save()
        return updates

    def add(self, pkg, target, version):
        if target not in self.pkgs:
            self.pkgs[target] = {}
        self.pkgs[target][pkg] = version
        self.save()

    def save(self):
        with open(FILENAME, 'w') as stream:
            yaml.dump(self.pkgs, stream, default_flow_style=False)
            stream.close()

    def install(self, ipkgs, target):
        pkgs = {}
        if len(ipkgs) == 0: # no argument supplied, try to install from config
            pkgs = self.pkgs
        else:
            for pkg in ipkgs:
                if not target in pkgs:
                    pkgs[target] = {}
                pkgs[target][pkg] = str(self.updater.get_last_version(pkg))
                if target:
                    self.add(pkg, target, pkgs[target][pkg])

        installs = []
        for target in pkgs:
            for pkgver in pkgs[target].items():
                installs.append('=='.join(pkgver))

        pip.main(['install'] + installs)
        return pkgs

    def __str__(self):
        res = []
        for target in self.pkgs:
            res.append(target + ':')
            for requirement in self.pkgs[target]:
                version = self.pkgs[target][requirement]
                res.append('  - {0}@{1}'.format(requirement, version))
        return '\n'.join(res)
