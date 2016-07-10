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

from mqreceive.broker import Broker

class TestBroker(unittest.TestCase):
    def test_eq(self):
        a = Broker("broker-a", "127.0.0.1", 1883)
        b = Broker("broker-a", "127.0.0.1", 1883)
        self.assertEqual(a, b)
    def test_eq_name(self):
        a = Broker("broker-a", "127.0.0.1", 1883)
        b = Broker("broker-b", "127.0.0.1", 1883)
        self.assertNotEqual(a, b)
    def test_eq_host(self):
        a = Broker("broker-a", "127.0.0.1", 1883)
        b = Broker("broker-a", "127.0.0.2", 1883)
        self.assertNotEqual(a, b)
    def test_eq_port(self):
        a = Broker("broker-a", "127.0.0.1", 1883)
        b = Broker("broker-a", "127.0.0.1", 1884)
        self.assertNotEqual(a, b)
