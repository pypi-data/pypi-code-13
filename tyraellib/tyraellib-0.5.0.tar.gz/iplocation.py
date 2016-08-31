#!/usr/bin/env python
# encoding: utf-8
import json
from urlparse import urljoin

from http import HttpBaseObject


class IpLocation(HttpBaseObject):
    QUERY_IP_URL = "http://ip-api.com/json/"
    def query_ip_geo(self, ip):
        url = urljoin(self.QUERY_IP_URL, ip)
        rsp = self.url_get_content(url, data={})
        if rsp:
            return json.loads(rsp)
        else:
            return rsp

if __name__ == '__main__':
    il = IpLocation()
    print il.query_ip_geo('8.8.8.8')
