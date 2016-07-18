import logging

import time

from dateutil.parser import parse
from isa.plugin import Plugin

_logger = logging.getLogger(__name__)


def plugin_init(args):
    return Collectl(args.interval)


class Collectl(Plugin):
    def __init__(self, timewindow=None):
        self.timewindow = timewindow

    def collect(self, server):
        """
        Execute collectl on the server.

        :return: list of result objects (list of dictionaries)
        """
        timewindow_str = ""
        if self.timewindow is not None and self.timewindow > 0:
            timewindow_str = "-i%s" % self.timewindow
        command = "collectl -c1 --all %s" % timewindow_str
        server.bash = "[\#].*\n[^\#].*\n.*[\#\$]"
        _logger.debug(command)
        result = server.execute(command)
        parsed = self.parse_collectl(result)
        return [parsed]

    @staticmethod
    def parse_collectl(str):
        """
        Parse the raw response from collectl.

        :param str: raw response from collectl
        :return: dictionary containing the results
        """
        lines = str.replace("\r", "").split("\n")
        first = True
        for line in lines[::-1]:
            if len(line) > 0:
                if first:
                    data = line.split()
                    first = False
                else:
                    if line[0] == '#':
                        line = line[1:]
                        header = line.split()
                        result = {key: value for key, value in zip(header, data)}
                        break
        return result
