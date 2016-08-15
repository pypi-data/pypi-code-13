#!/usr/bin/env python
""" Simple/Pythonic Zeroconf Service Search/Registration """

import sh
import subprocess
from . import decode, ZeroConfBase, name_match, NAMES

if not sh.which("avahi-browse"):
    raise ImportError("Unable to find avahi command-line tools")


class ZeroConf(ZeroConfBase):
    """
        Linux implementation of ZeroConf base

        >>> import time
        >>> import sys

        Register a new (fake) HTTP server
        >>> zc = ZeroConf()
        >>> zc.register(name="webserver", type="_http._tcp", port="49152")
        >>> time.sleep(1.0)

        Basic search (fully specified):
        >>> services = zc.search("webserver", "_http._tcp", "local")
        >>> info = services.get(("webserver", "_http._tcp", "local"))
        >>> info is not None
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

    def register(self, name=None, type=None, port=None):
        """ Register a new service """
        args = ["avahi-publish", "-s", name, type, port]
        publisher = subprocess.Popen(args, stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        self._publishers[(name, type, port)] = publisher

    def search(self, name=None, type=None, domain="local"):
        """
            Search for a service in specified domain
        """
        options = {"terminate": True, "resolve": True, "parsable": True,
                   "no-db-lookup": True, "domain": domain}
        if type:
            results = sh.avahi_browse(type, **options).splitlines()
        else:
            results = sh.avahi_browse(all=True, **options).splitlines()

        info = {}
        for result in [line.split(';') for line in results]:
            if result[0] == "=":
                ip_version, name_, type, domain_ = result[2:6]
                name_ = decode(name_)

                if ip_version != "IPv4":
                    continue

                info[(name_, type, domain_)] = dict(zip(NAMES, result[6:]))

        filtered_info = [i for i in info.items() if name_match(name, i[0])]
        return dict(filtered_info)
