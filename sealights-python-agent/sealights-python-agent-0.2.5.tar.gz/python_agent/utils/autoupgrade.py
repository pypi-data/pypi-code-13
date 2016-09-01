import os
import sys
import logging

import pkg_resources
import pip

from python_agent import semantic_version
from python_agent import requests

log = logging.getLogger(__name__)


class AutoUpgrade(object):
    def __init__(self, pkg, server, customer_id):
        self.pkg = pkg
        self.server = server
        self.customer_id = customer_id

    def get_recommended_version(self):
        url = ""
        params = {}
        try:
            url = "/".join([self.server, "v1", "agents", self.pkg, "recommended"])
            params = {"customerId": self.customer_id}
            response = requests.get(url, params=params)
            response.raise_for_status()
            version = response.json().get("agent", {}).get("version")
            return semantic_version.Version(version)
        except Exception as e:
            log.exception("failed getting recommended version. url: %s. params: %s. error: %s" % (url, params, str(e)))
        return semantic_version.Version("0.0.0")

    def get_current_version(self):
        current_version = pkg_resources.get_distribution(self.pkg).version
        current_version = semantic_version.Version(current_version)
        return current_version

    def check(self):
        current_version = self.get_current_version()
        recommended_version = self.get_recommended_version()
        return recommended_version > current_version

    def upgrade(self):
        if self.check():
            status = 1
            try:
                status = pip.main(["install", self.pkg + "==" + str(self.get_recommended_version()), "--ignore-installed"])
            except SystemExit:
                return
            if status == 0:
                self.restart()

    def restart(self):
        os.execl(sys.executable, *([sys.executable] + sys.argv))

    def remove_compiled_files(self):
        top_level = __name__.split('.')[0]
        site_packages = pkg_resources.get_distribution(self.pkg).location
        directory = os.listdir(site_packages + "/" + top_level)
        for filename in directory:
            if filename[-3:] == 'pyc':
                print '- ' + filename
                os.remove(filename)
