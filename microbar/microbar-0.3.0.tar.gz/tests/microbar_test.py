from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest.case import TestCase

from microbar.microbar import MicroBar


class PublicApiTests(TestCase):

    number_bars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    def test_instanciation_min_value(self):
        minimum = '0'
        maximum = 9

        with self.assertRaises(TypeError):
            MicroBar(minimum=minimum, maximum=maximum)

    def test_instanciation_max_value(self):
        minimum = 0
        maximum = '9'

        with self.assertRaises(TypeError):
            MicroBar(minimum=minimum, maximum=maximum)

    def test_instanciation_min_max(self):
        minimum = 9
        maximum = 0

        with self.assertRaises(ValueError):
            MicroBar(minimum=minimum, maximum=maximum)

    def test_instanciation_bars_type(self):
        minimum = 0
        maximum = 9
        bars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        with self.assertRaises(TypeError):
            MicroBar(minimum=minimum, maximum=maximum, bars=bars)

    def test_microbar_ints(self):
        minimum = 0
        maximum = 9
        bars = self.number_bars

        microbar = MicroBar(minimum=minimum, maximum=maximum, bars=bars)

        assert microbar.get_bar(value=0) == '0'
        assert microbar.get_bar(value=1) == '1'
        assert microbar.get_bar(value=2) == '2'
        assert microbar.get_bar(value=3) == '3'
        assert microbar.get_bar(value=4) == '4'
        assert microbar.get_bar(value=5) == '5'
        assert microbar.get_bar(value=6) == '6'
        assert microbar.get_bar(value=7) == '7'
        assert microbar.get_bar(value=8) == '8'
        assert microbar.get_bar(value=9) == '9'

    def test_microbar_floats(self):
        minimum = 0.0
        maximum = 0.9
        bars = self.number_bars

        microbar = MicroBar(minimum=minimum, maximum=maximum, bars=bars)

        assert microbar.get_bar(value=0.0) == '0'
        assert microbar.get_bar(value=0.1) == '1'
        assert microbar.get_bar(value=0.2) == '2'
        assert microbar.get_bar(value=0.3) == '3'
        assert microbar.get_bar(value=0.4) == '4'
        assert microbar.get_bar(value=0.5) == '5'
        assert microbar.get_bar(value=0.6) == '6'
        assert microbar.get_bar(value=0.7) == '7'
        assert microbar.get_bar(value=0.8) == '8'
        assert microbar.get_bar(value=0.9) == '9'
