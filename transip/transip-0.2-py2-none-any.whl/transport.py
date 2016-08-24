# python-transip is a Python implementation of the TransIP SOAP API
#
# Copyright (c) 2016 Nick Douma <n.douma@nekoconeko.nl>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

import requests

try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

PROXIES = None


def set_proxies(proxies):
    global PROXIES
    PROXIES = proxies

from io import StringIO
from suds.transport.http import HttpAuthenticated
from suds.transport import Reply


class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self.cacert = kwargs.pop('cacert', None)
        self.timeout = kwargs.pop('timeout', None)
        # super won't work because not using new style class
        HttpAuthenticated.__init__(self, **kwargs)

    def open(self, request):
        self.addcredentials(request)
        resp = requests.get(request.url, data=request.message,
                            headers=request.headers,
                            verify=self.cacert or False,
                            proxies=PROXIES, timeout=self.timeout)
        result = StringIO(resp.content.decode('utf-8'))
        return result

    def send(self, request):
        self.addcredentials(request)
        resp = requests.post(request.url, data=request.message,
                             headers=request.headers,
                             verify=self.cacert or False,
                             proxies=PROXIES, timeout=self.timeout)
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result
