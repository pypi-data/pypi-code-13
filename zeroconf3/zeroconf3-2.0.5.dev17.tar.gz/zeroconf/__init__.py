#!/usr/bin/env python
# coding: utf-8

""" Simple/Pythonic Zeroconf Service Search/Registration """

import re
import sys
import atexit


NAMES = ["hostname", "address", "port", "txt"]


def name_match(name, service):
    """ Match name """
    name_, _, _ = service
    return name is None or name_ == name


def decode(text):
    r"""
Decode string with special characters escape sequences.

We assume that the escaping scheme follows the rules used by `avahi-browse`
when the `--parsable` option is enabled
(see `avahi_escape_label` function in `avahi-common/domain.c`).

    >>> decode("abc")
    'abc'
    >>> decode(r"a\.c")
    'a.c'
    >>> decode(r"a\\c")
    'a\\c'
    >>> decode(r"a\032c")
    'a c'
    >>> decode(r"a\127c")
    'a\x7fc'

Characters may go beyond the 0-127 (ascii) range:
for example, the 'RIGHT SINGLE QUOTATION MARK',
encoded in utf-8 by the three bytes 226, 128 and 153 (decimal):

    >>> decode(r"\226\128\153")
    '\xe2\x80\x99'

Input strings in unicode are ok as long as they belong to the ascii range:

    >>> decode(r"\226\128\153")
    '\xe2\x80\x99'
"""
    text = text.encode("ascii")

    def replace(match):
        """ replace """
        numeric, other = match.groups()
        if numeric:
            if sys.version_info[0] < 3:
                return chr(int(numeric[1:]))
            else:
                return bytes(chr(int(numeric[1:])), 'utf-8')
        else:
            return other[1:]

    if sys.version_info[0] < 3:
        return re.sub(r"(\\\d\d\d)|(\\.)", replace, text)
    else:
        return re.sub(bytes(r"(\\\d\d\d)|(\\.)", 'utf-8'),
                      replace, text).decode()


class ZeroConfBase(object):
    """ Base zeroconf object, all implementations must inherit from this """

    _publishers = {}

    def __init__(self):
        atexit.register(self.unregister)

    def register(self, name, type, port):
        """ Register a new service """
        values = name, type, str(port)
        assert values not in self._publishers, "Already registered"

    def unregister(self, name=None, type=None, port=None):
        """
            When an argument is omitted, it will attempt to unregister
            all services that match the remaining arguments, or all services if
            no arguments are provided.

            The unregistration is limited to services whose registration comes
            from the same instance of the zeroconf module.
        """

        def _match(query, value):
            """If we've got a match filter, apply it. Otherwise return True"""
            return query is None or str(query) == str(value)

        deleted = False
        search = (name, type, port)
        to_delete = []

        for values in self._publishers:
            if all([_match(n, v) for n, v in list(zip(search, values))]):
                self._publishers[values].kill()
                deleted = True
                to_delete.append(values)

        for value in to_delete:
            del self._publishers[value]

        return deleted

    def search(self, name, type, domain):
        """
            Search for a service in specified domain
            The result is a dictionary with service (name, type, domain) keys
            and data values ; data are dictionaries with "hostname", "address",
            "port" and "txt" keys.
        """
        raise NotImplementedError()


if sys.platform.startswith("linux"):
    from zeroconf.linux import ZeroConf

elif sys.platform.startswith("win"):
    from zeroconf.windows import ZeroConf


if __name__ == "__main__":
    ZeroConf()  #: noqa
