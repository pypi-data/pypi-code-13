# -*- coding: utf-8 -*-
from unittest import TestCase

from serpost.serpost import format_date


class FormatDateTestCase(TestCase):

    def test_date_format_1_am(self):
        example = '15/08/2014 03:08:00 p.m.'
        result = format_date(example)
        self.assertIsNotNone(result)

    def test_date_format_1_pm(self):
        example = '15/08/2014 03:08:00 a.m.'
        result = format_date(example)
        self.assertIsNotNone(result)

    def test_date_format_2_day(self):
        example = '26/08/2016 - 08:50'
        result = format_date(example)
        self.assertIsNotNone(result)

    def test_date_format_2_night(self):
        example = '26/08/2016 - 16:50'
        result = format_date(example)
        self.assertIsNotNone(result)

    def test_unknown_format(self):
        example = '26/08/2016 / 16:50'
        result = format_date(example)
        self.assertIsNone(result)
