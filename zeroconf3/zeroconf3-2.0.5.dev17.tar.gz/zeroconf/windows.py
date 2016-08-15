#!/usr/bin/env python
""" Simple/Pythonic Zeroconf Service Search/Registration """

import subprocess
import time
from . import decode, ZeroConfBase, NAMES, name_match

if not getattr(__builtins__, "WindowsError", None):
    class WindowsError(OSError):
        """ Emulate windows error class for autodoc and such """
        pass

try:
    STARTUPINFO = subprocess.startupinfo()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen("dns-sd", startupinfo=STARTUPINFO).kill()
except WindowsError:
    raise ImportError("Unable to find dns-sd command-line tools")
except AttributeError:
    pass  # Importing from linux


def get_address(hostname):
    """
        Get an address for a specific hostname
    """
    process = subprocess.Popen("dns-sd -Q " + hostname,
                               stdout=subprocess.PIPE, startupinfo=STARTUPINFO)
    time.sleep(0.1)
    process.kill()
    results = process.stdout.read().decode()
    results = [line.split() for line in results.splitlines()]

    if len(results) >= 1:
        return results[1][len(results[1]) - 1]

    return ''


class ZeroConf(ZeroConfBase):
    """
        Windows implementation of ZeroConf base

        >>> import time
        >>> import sys

        Register a new (fake) HTTP server
        >>> zc = ZeroConf()
        >>> zc.register(name="webserver", type="_http._tcp", port="49152")
        >>> time.sleep(1.0)

        Basic search (fully specified):
        >>>  services = zc.search("webserver", "_http._tcp", "local")
        >>>  info = services.get(("webserver", "_http._tcp", "local"))
        >>>  info is not None
        True

        >>> info['txt'] == ''
        True

        >>> info["port"] == "49152"
        True

        The `domain` argument is optional and defaults to "local":
        >>> zc.search("webserver", "_http._tcp") == services
        True

        When the `type` argument is not given, all service
        types are considered:
        >>> zc.search("webserver") == services
        True

        The service `name` is optional too:
        >>> http_services = zc.search(type="_http._tcp")
        >>> list(services.items())[0] in http_services.items()
        True

        Unregister the HTTP server:
        >>> zc.unregister(name="webserver", type="_http._tcp",
        ...               port="49152")
        True

        >>> time.sleep(1.0)
        >>> not zc.search("webserver", "_http._tcp")
        True


    """
    def register(self, name, type, port):
        """ Register a new service """
        args = 'dns-sd -R "' + name + '" ' + type + " local " + port
        publisher = subprocess.Popen(args, stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     startupinfo=STARTUPINFO)
        self._publishers[(name, type, port)] = publisher

    def search(self, name, type="_http._tcp", domain="local"):
        """
            Search for a service in specified domain
            This does pretty awful stuff to parse windows format
        """

        process = subprocess.Popen("dns-sd -Z " + type + " " + domain,
                                   stdout=subprocess.PIPE,
                                   startupinfo=STARTUPINFO)
        time.sleep(1.0)
        process.kill()
        results = process.stdout.read().decode()
        results = [line.split() for line in results.splitlines()]

        info = {}

        name_ = port = hostname = address = ""

        for result in results:
            if len(result) == 14 and result[1] == "SRV":
                name_ = decode(result[0]).split(".")[0]
                port, hostname = result[4:6]
                address = get_address(hostname)
                type = decode(result[0])[(decode(result[0]).find(".") + 1):]

            if len(result) == 3 and result[1] == "TXT":
                txt = str.replace(result[2], '"', '')
                values = hostname, address, port, txt
                info[(name_, type, domain)] = zip(NAMES, values)

        filtered_info = [i for i in info.items() if name_match(name, i[0])]
        return dict(filtered_info)
