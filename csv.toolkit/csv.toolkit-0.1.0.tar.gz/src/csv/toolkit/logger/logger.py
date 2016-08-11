#
# Copyright (c) 2016, Michael Conroy
#


import six


__all__ = ('SimpleLogger',)


class SimpleLogger(object):
    """
    Simple logging container for logging messages.

    This class allows logging of messages in an internal list. The messages
    are available for output. Output may be a string with newline characters
    separating each log, or output may be the internal list of logs. All
    messages may be cleared.

    Make sure logs are cleared in each logging instance when the logging
    instance is no longer needed or needs to be reset.
    """

    __slots__ = ('_logs',)

    def __init__(self):
        self._logs = []

    def clear(self):
        self._logs = []

    @property
    def logs(self):
        return "\n".join(self._logs)

    def log(self, inlog):
        if not isinstance(inlog, six.string_types):
            raise ValueError('Loggable objects must be of type string')
        return self._logs.append(inlog)

    def check(self):
        """ Checks if any logs have been registered. """
        if len(self._logs) == 0:
            return False
        else:
            return True
