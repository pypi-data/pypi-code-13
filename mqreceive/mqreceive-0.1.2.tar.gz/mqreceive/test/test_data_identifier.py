# Copyright (C) Ivo Slanina <ivo.slanina@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from mqreceive.data import DataIdentifier
from mqreceive.broker import Broker

class TestDataIdentifier(unittest.TestCase):
    def setUp(self):
        self.broker = Broker("test-broker", "127.0.0.1", 1883)
        self.topic = "test/topic"
        self.dataIdentifier = DataIdentifier(self.broker, self.topic)
    def test_init(self):
        self.assertEqual(self.dataIdentifier.broker, self.broker)
        self.assertEqual(self.dataIdentifier.topic, self.topic)
    def test_eq(self):
        broker = Broker(self.broker.name, self.broker.host, self.broker.port)
        di = DataIdentifier(broker, self.topic)
        self.assertEqual(self.dataIdentifier, di)
    def test_eq_broker_name(self):
        broker = Broker(self.broker.name[::-1], self.broker.host, self.broker.port)
        di = DataIdentifier(broker, self.topic)
        self.assertNotEqual(self.dataIdentifier, di)
    def test_eq_broker_host(self):
        broker = Broker(self.broker.name, self.broker.host[::-1], self.broker.port)
        di = DataIdentifier(broker, self.topic)
        self.assertNotEqual(self.dataIdentifier, di)
    def test_eq_broker_port(self):
        broker = Broker(self.broker.name, self.broker.host, self.broker.port + 1)
        di = DataIdentifier(broker, self.topic)
        self.assertNotEqual(self.dataIdentifier, di)
