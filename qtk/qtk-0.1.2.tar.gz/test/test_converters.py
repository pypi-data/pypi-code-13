from qtk.converters import QuantLibConverter
from unittest import TestCase
import QuantLib as ql
from qtk.templates import Template


class TestConverter(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert_daycount(self):
        keys = QuantLibConverter._daycount_map.keys()
        vals = QuantLibConverter._daycount_map.values()

        for key, val in QuantLibConverter._daycount_map.iteritems():
            dc = QuantLibConverter.to_daycount(key)
            self.assertTrue(dc == val)
            dc = QuantLibConverter.to_daycount(val)
            self.assertTrue(dc == val)

        dc_choices = ["ACT/ACT", "ACT/ACT (BOND)", "30/360", "ACT/365", "Actual/365 (Fixed)", "NL/365"]
        dc_values = [ql.ActualActual(),
                       ql.ActualActual(ql.ActualActual.Bond),
                       ql.Thirty360(),
                       ql.ActualActual(),
                       ql.Actual365Fixed(),
                       ql.Actual365NoLeap()]
        for dc_choice, dc_value in zip(dc_choices, dc_values):
            dc = QuantLibConverter.to_daycount(dc_choice)
            self.assertTrue(dc == dc_value)

    def test_convert_date(self):
        expected = ql.Date(1, 5, 2016)
        date = QuantLibConverter.to_date("5/1/2016")
        self.assertTrue(date == expected)

        date = QuantLibConverter.to_date(expected)
        self.assertTrue(date == expected)

        date = QuantLibConverter.to_date("05-01-2016")
        self.assertTrue(date == expected)

        date = QuantLibConverter.to_date("May 1, 2016")
        self.assertTrue(date == expected)

        import datetime
        date = QuantLibConverter.to_date(datetime.date(2016, 5, 1))
        self.assertTrue(date == expected)

    def test_convert_template(self):
        expected = Template.TS_YIELD_BOND
        template = QuantLibConverter.to_template(Template.TS_YIELD_BOND.id)
        self.assertEqual(template, expected)

    def test_convert_date_generation(self):
        dg = ["BACKWARD", "FORWARD", "ZERO", "THIRDWEDNESDAY", "TWENTIETH", "TWENTIETHIMM", "OLDCDS", "CDS"]
        val = range(0,8)
        for d, expected in zip(dg, val):
            observed = QuantLibConverter.to_date_generation(d)
            self.assertEqual(observed, expected)

