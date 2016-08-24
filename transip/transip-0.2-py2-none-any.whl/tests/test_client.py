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

from collections import OrderedDict
from transip.client import parameters_encode

SERVICE = "service"
METHOD = "method"
HOSTNAME = "hostname"
TIMESTAMP = "timestamp"
NONCE = "nonce"

PARAMETER_TESTS = [
    (
        [],
        ""
    ),
    (
        ["value"],
        "0=value"
    ),
    (
        ["bar", "baz"],
        "0=bar&1=baz"
    ),
    (
        ["value", "bar", "baz"],
        "0=value&1=bar&2=baz"
    ),
    (
        [
            [
                OrderedDict([("bar", "baz"), ("foo", "bar")]),
            ],
            "bar"
        ],
        "0[0][bar]=baz&0[0][foo]=bar&1=bar"
    ),
    (
        [
            [
                OrderedDict([("foo", "bar")]),
                OrderedDict([("foo", "bar")]),
                OrderedDict([("foo", "bar")]),
                OrderedDict([("foo", "bar")]),
            ],
            "bar"
        ],
        "0[0][foo]=bar&0[1][foo]=bar&0[2][foo]=bar&0[3][foo]=bar&1=bar"
    ),
    (
        [
            "example.com",
            [
                OrderedDict([("name", "@"), ("expire", 86400), ("type", "A"), ("content", "127.0.0.1")]),
                OrderedDict([("name", "www"), ("expire", 86400), ("type", "CNAME"), ("content", "@")]),
                OrderedDict([("name", "mail"), ("expire", 86400), ("type", "CNAME"), ("content", "@")]),
                OrderedDict([("name", "@"), ("expire", 86400), ("type", "MX"), ("content", "10 mail.")]),
            ]
        ],
        "0=example.com&"
        "1[0][name]=%40&1[0][expire]=86400&1[0][type]=A&1[0][content]=127.0.0.1&"
        "1[1][name]=www&1[1][expire]=86400&1[1][type]=CNAME&1[1][content]=%40&"
        "1[2][name]=mail&1[2][expire]=86400&1[2][type]=CNAME&1[2][content]=%40&"
        "1[3][name]=%40&1[3][expire]=86400&1[3][type]=MX&1[3][content]=10%20mail."
    ),
    (
        [
            "example.com",
            [
                OrderedDict([("name", "@"), ("expire", 86400), ("type", "A"), ("content", "127.0.0.1")]),
                OrderedDict([("name", "@"), ("expire", 60), ("type", "MX"), ("content", "10 mxa.mail.org.")]),
                OrderedDict([("name", "@"), ("expire", 60), ("type", "MX"), ("content", "10 mxb.mail.org.")]),
                OrderedDict([("name", "@"), ("expire", 60), ("type", "TXT"), ("content", "v=spf1 include:mail.org ~all")]),
                OrderedDict([("name", "blog"), ("expire", 86400), ("type", "CNAME"), ("content", "foo.example.com.")]),
                OrderedDict([("name", "email"), ("expire", 60), ("type", "CNAME"), ("content", "mail.org.")]),
                OrderedDict([("name", "is"), ("expire", 86400), ("type", "CNAME"), ("content", "foo.example.com.")]),
                OrderedDict([("name", "smtp._domainkey"), ("expire", 60), ("type", "TXT"), ("content", "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIfZ+lDFI4g1Zha6866T7sKcrq5ZpcArnTN8Z43lFbl/wNnvxpB81Dh1L9WtySrQ8kozA7HX8uSzcCOWXYam/U9T9HmitJ7pua48ncMrK0vIfJsk9UmSr2lkpGk7VIrUk4LhSlIsIcmEL2y0VMaGjgB+G8Tu8h+eFLbPl7MxyMSwIDAQAB")]),
                OrderedDict([("name", "www"), ("expire", 86400), ("type", "CNAME"), ("content", "foo.example.com.")]),
            ]
        ],
        "0=example.com&"
        "1[0][name]=%40&1[0][expire]=86400&1[0][type]=A&1[0][content]=127.0.0.1&"
        "1[1][name]=%40&1[1][expire]=60&1[1][type]=MX&1[1][content]=10%20mxa.mail.org.&"
        "1[2][name]=%40&1[2][expire]=60&1[2][type]=MX&1[2][content]=10%20mxb.mail.org.&"
        "1[3][name]=%40&1[3][expire]=60&1[3][type]=TXT&1[3][content]=v%3Dspf1%20include%3Amail.org%20~all&"
        "1[4][name]=blog&1[4][expire]=86400&1[4][type]=CNAME&1[4][content]=foo.example.com.&"
        "1[5][name]=email&1[5][expire]=60&1[5][type]=CNAME&1[5][content]=mail.org.&"
        "1[6][name]=is&1[6][expire]=86400&1[6][type]=CNAME&1[6][content]=foo.example.com.&"
        "1[7][name]=smtp._domainkey&1[7][expire]=60&1[7][type]=TXT&1[7][content]=k%3Drsa%3B%20p%3DMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIfZ%2BlDFI4g1Zha6866T7sKcrq5ZpcArnTN8Z43lFbl%2FwNnvxpB81Dh1L9WtySrQ8kozA7HX8uSzcCOWXYam%2FU9T9HmitJ7pua48ncMrK0vIfJsk9UmSr2lkpGk7VIrUk4LhSlIsIcmEL2y0VMaGjgB%2BG8Tu8h%2BeFLbPl7MxyMSwIDAQAB&"
        "1[8][name]=www&1[8][expire]=86400&1[8][type]=CNAME&1[8][content]=foo.example.com."
    )
]


def _test_parameters_encode(_in, _out, include_meta):
    _output = parameters_encode(
        service=SERVICE,
        method=METHOD,
        hostname=HOSTNAME,
        timestamp=TIMESTAMP,
        nonce=NONCE,
        additional=_in,
        include_meta=include_meta)
    if include_meta:
        if not _in:
            # Testing the empty case with metadata makes no sense
            return True

        meta = "__method={}&__service={}&__hostname={}&__timestamp={}&__nonce={}"\
            .format(METHOD, SERVICE, HOSTNAME, TIMESTAMP, NONCE)
        assert _output == "&".join([_out, meta]), \
            "{0} does not match {1}".format(_output, "&".join([_out, meta]))

    else:
        assert _output == _out, \
            "{0} does not match {1}".format(_output, _out)


def test_parameters_should_encode():
    for _in, _out in PARAMETER_TESTS:
        yield (_test_parameters_encode, _in, _out, False)


def test_parameters_should_encode_with_metadata():
    for _in, _out in PARAMETER_TESTS:
        yield (_test_parameters_encode, _in, _out, True)
