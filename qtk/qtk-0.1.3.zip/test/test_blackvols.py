from unittest import TestCase
import QuantLib as ql
from qtk import Controller


class BlackVolTest(TestCase):

    def test_constant_vol(self):
        asof_date = "8/15/2016"
        data =[
            {'AsOfDate': "8/15/2016",
             'Basis': "ACT/ACT",
             'Calendar': "UnitedStates",
             'ObjectId': "BlackConstantVol",
             'Template': "TermStructure.Volatility.BlackConstant",
             'Volatility': 0.45}
        ]
        c = Controller(data)
        c.process(asof_date)
        obj = c.object("BlackConstantVol")
        self.assertIsInstance(obj, ql.BlackConstantVol)

    def test_vol_curve(self):
        asof_date = "8/15/2016"
        data = [
            {'AsOfDate': asof_date,
             'Basis': "ACT/ACT",
             'ListOfDate': ["8/15/2017", "8/15/2018","8/15/2019"],
             'ListOfVolatility': [0.45, 0.45, 0.45],
             'ObjectId': "BlackVolCurve",
             'Template': 'TermStructure.Volatility.BlackCurve'}
        ]
        c = Controller(data)
        c.process(asof_date)
        obj = c.object("BlackVolCurve")
        self.assertIsInstance(obj, ql.BlackVarianceCurve)

    def test_vol_surface(self):
        asof_date = "8/15/2016"
        data = [
            {'Basis': 'ACT/ACT',
             'Calendar': 'UnitedStates',
             'ListOfDate': ["8/15/2017", "8/15/2018","8/15/2019"],
             'ListOfListOfVolatility': [["0.45", "0.45"], ["0.45","0.45"], ["0.45", "0.45"]],
             'ListOfStrike': ["100", "110"],
             'ObjectId': 'BlackVolSurface',
             'AsOfDate': asof_date,
             'Template': 'TermStructure.Volatility.BlackSurface'}
        ]
        c = Controller(data)
        c.process(asof_date)
        obj = c.object("BlackVolSurface")
        self.assertIsInstance(obj, ql.BlackVarianceSurface)