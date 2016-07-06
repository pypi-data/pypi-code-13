# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
Test cases for twisted.protocols.stateful
"""

from twisted.trial.unittest import TestCase
from twisted.protocols.test import test_basic
from twisted.protocols.stateful import StatefulProtocol

from struct import pack, unpack, calcsize


class MyInt32StringReceiver(StatefulProtocol):
    """
    A stateful Int32StringReceiver.
    """
    MAX_LENGTH = 99999
    structFormat = "!I"
    prefixLength = calcsize(structFormat)

    def getInitialState(self):
        return self._getHeader, 4

    def lengthLimitExceeded(self, length):
        self.transport.loseConnection()

    def _getHeader(self, msg):
        length, = unpack("!i", msg)
        if length > self.MAX_LENGTH:
            self.lengthLimitExceeded(length)
            return
        return self._getString, length

    def _getString(self, msg):
        self.stringReceived(msg)
        return self._getHeader, 4

    def stringReceived(self, msg):
        """
        Override this.
        """
        raise NotImplementedError

    def sendString(self, data):
        """
        Send an int32-prefixed string to the other end of the connection.
        """
        self.transport.write(pack(self.structFormat, len(data)) + data)


class TestInt32(MyInt32StringReceiver):
    def connectionMade(self):
        self.received = []

    def stringReceived(self, s):
        self.received.append(s)

    MAX_LENGTH = 50
    closed = 0

    def connectionLost(self, reason):
        self.closed = 1


class Int32Tests(TestCase, test_basic.IntNTestCaseMixin):
    protocol = TestInt32
    strings = ["a", "b" * 16]
    illegalStrings = ["\x10\x00\x00\x00aaaaaa"]
    partialStrings = ["\x00\x00\x00", "hello there", ""]

    def test_bigReceive(self):
        r = self.getProtocol()
        big = ""
        for s in self.strings * 4:
            big += pack("!i", len(s)) + s
        r.dataReceived(big)
        self.assertEqual(r.received, self.strings * 4)

