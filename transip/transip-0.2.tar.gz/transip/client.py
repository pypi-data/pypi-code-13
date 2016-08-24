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

from .transport import RequestsTransport
from collections import OrderedDict
from hashlib import sha512
from M2Crypto import RSA
import suds
from suds.xsd.doctor import ImportDoctor, Import
from suds.sudsobject import Object as SudsObject, asdict as SudsDict
import time
import urllib
import uuid

ASN1_HEADER = b"\x30\x51\x30\x0D\x06\x09\x60\x86\x48" + \
              b"\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40"


def parameters_encode(service, method, hostname, timestamp, nonce,
                      additional=None, include_meta=True):
    if additional is None:
        additional = []

    sign = OrderedDict()
    # Add all additional parameters first
    for index, value in enumerate(additional):
        if isinstance(value, list):
            for entryindex, entryvalue in enumerate(value):
                if isinstance(entryvalue, SudsObject):
                    entryvalue = SudsDict(entryvalue)
                for objectkey, objectvalue in entryvalue.iteritems():
                    sign[str(index) + '[' + str(entryindex) + '][' +
                         objectkey + ']'] = objectvalue
        else:
            sign[index] = value

    if include_meta:
        sign['__method'] = method
        sign['__service'] = service
        sign['__hostname'] = hostname
        sign['__timestamp'] = timestamp
        sign['__nonce'] = nonce

    return urlencode(sign).replace('%5B', '[').replace('%5D', ']')


def urlencode(payload):
    """
    TransIP's PHP client has a specific expection to the encoding of
    "~". Not sure why, but lets replicate it for compatability.
    """
    _payload = ["{0}={1}".format(k, urllib.quote(str(v), ''))
                for k, v in payload.iteritems()]
    return "&".join(_payload).replace('%7E', '~')


class TransIpClient(object):
    service = None
    api_version = "5.2"

    def __init__(self, username, key_file, endpoint='api.transip.nl',
                 mode="readonly", **kwargs):
        if not hasattr(key_file, "read"):
            key_file = open(key_file, "rb")

        self.endpoint = endpoint
        self.username = username
        self.mode = mode

        self.key = key_file.read()\
            .replace("BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY")\
            .replace("END PRIVATE KEY", "END RSA PRIVATE KEY")
        key_file.close()

        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        doc = ImportDoctor(imp)
        transport = RequestsTransport(**kwargs)
        self.client = suds.client.Client(self._build_service_uri(), doctor=doc,
                                         transport=transport, cache=None)

    def _build_service_uri(self):
        if not self.service:
            raise RuntimeError("Please do not use TransIpClient directly.")

        return "https://{0}/wsdl/?service={1}"\
               .format(self.endpoint, self.service)

    def _build_request_cookie(self, timestamp=None, nonce=None, method=None,
                              parameters=None):
        if not timestamp:
            timestamp = int(time.time())
        if not nonce:
            nonce = str(uuid.uuid4())[:32]
        signature = self._sign(timestamp, nonce, method, parameters)

        cookie = OrderedDict()
        cookie["login"] = self.username
        cookie["mode"] = self.mode
        cookie["timestamp"] = timestamp
        cookie["nonce"] = nonce
        cookie["clientVersion"] = self.api_version
        cookie["signature"] = urllib.quote_plus(signature)

        cookie = ["{0}={1};".format(k, v) for k, v in cookie.iteritems()]
        return " ".join(cookie)

    def _sign(self, timestamp, nonce, method, parameters):
        params = parameters_encode(
            service=self.service,
            method=method,
            hostname=self.endpoint,
            timestamp=timestamp,
            nonce=nonce,
            additional=parameters)

        digest = ASN1_HEADER + \
            sha512(params).digest()

        rsa = RSA.load_key_string(self.key)
        signature = rsa.private_encrypt(digest, RSA.pkcs1_padding)
        return signature.encode('base64').replace("\n", "")

    def __getattr__(self, _attr):
        def _soap_action(*args):
            self.client.set_options(
                headers={'Cookie': self._build_request_cookie(method=_attr,
                         parameters=args)})
            return getattr(self.client.service, _attr)(*args)
        return _soap_action


class DomainClient(TransIpClient):
    service = "DomainService"

    def setDnsEntries(self, zone, entries):
        _entries = []
        for entry in entries:
            _entry = OrderedDict([
                ("name", entry['name']),
                ("expire", entry['expire']),
                ("type", entry['type']),
                ("content", entry['content'])
            ])
            _entries.append(_entry)
        super(DomainClient, self).__getattr__("setDnsEntries")(zone, _entries)
