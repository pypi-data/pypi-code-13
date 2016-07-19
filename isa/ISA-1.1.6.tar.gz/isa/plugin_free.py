import logging

import time

from dateutil.parser import parse
from isa.plugin import Plugin

_logger = logging.getLogger(__name__)


def plugin_init(args):
    return Free(args.interval)


class Free(Plugin):
    def __init__(self, timewindow=None):
        self.timewindow = timewindow

    def collect(self, server):
        """
        Execute free -m on the server.

        :return: the resulting stats
        """
        command = "free -m"
        _logger.debug(command)
        result = server.execute(command)
        time.sleep(self.timewindow)
        return [self.parse_free(result)]

    @staticmethod
    def parse_free(str):
        """
        Parse the raw response from free -m.

        :param str: raw response from free -m
        :return: the resulting stats
        """
        lines = str.replace("\r", "").split("\n")
        header = None
        result = {}
        for line in lines:
            if len(line) > 0:
                parts = line.split()
                if header is None:
                    header = parts
                else:
                    key = parts[0]
                    tail = parts[1:]
                    try:
                        tail = [int(val) for val in tail]
                        for key, value in zip([key + h for h in header], tail):
                            result[key] = value
                    except ValueError:
                        pass
        return result
