from unittest import TestCase
from qtk import Controller


class TestOptions(TestCase):

    def test_european_option(self):
        asof_date = '5/8/2015'
        data = [
            {'MaturityDate': '1/15/2016',
             'ObjectId': 'EuropeanOption',
             'OptionType': 'Call',
             'Strike': 130,
             'PricingEngine': "->AnalyticEuropeanEngine",
             'Template': 'Instrument.Derivative.EuropeanOption'},
            {'AsOfDate': asof_date,
             'Basis': 'ACTUAL/365Fixed',
             'Calendar': 'UnitedStates',
             'DiscountRate': 0.001,
             'DividendRate': 0.0163,
             'ObjectId': 'BSMProcess',
             'Spot': 127.62,
             'Template': 'Process.Equity.BlackScholesMerton',
             'Volatility': 0.20},
            {'GeneralBlackScholesProcess': '->BSMProcess',
             'ObjectId': 'AnalyticEuropeanEngine',
             'Template': 'Engine.Equity.AnalyticEuropean'}
        ]

        controller = Controller(data)
        controller.process(asof_date)
        option = controller.object("EuropeanOption")
        npv = option.NPV()
        self.assertAlmostEqual(npv, 6.74927181246)

    def test_american_option(self):
        asof_date = '5/8/2015'
        data = [
            {'MaturityDate': '1/15/2016',
             'ObjectId': 'AmericanOption',
             'OptionType': 'Call',
             'Strike': 130,
             'PricingEngine': "->AmericanEngine",
             'Template': 'Instrument.Derivative.AmericanOption'},
            {'AsOfDate': asof_date,
             'Basis': 'ACTUAL/365Fixed',
             'Calendar': 'UnitedStates',
             'DiscountRate': 0.001,
             'DividendRate': 0.0163,
             'ObjectId': 'BSMProcess',
             'Spot': 127.62,
             'Template': 'Process.Equity.BlackScholesMerton',
             'Volatility': 0.20},
            {'GeneralBlackScholesProcess': '->BSMProcess',
             'ObjectId': 'AmericanEngine',
             'Template': 'Engine.Equity.FdAmerican'}
        ]

        controller = Controller(data)
        controller.process(asof_date)
        option = controller.object("AmericanOption")
        npv = option.NPV()
        self.assertAlmostEqual(npv, 6.83406034199118)

    def test_bermudan_option(self):
        asof_date = '5/8/2015'
        data = [
            {'MaturityDate': '1/15/2016',
             'ObjectId': 'BermudanOption',
             'OptionType': 'Call',
             'Strike': 130,
             'PricingEngine': "->BermudanEngine",
             "ListOfDate": ['11/15/2015','12/15/2015','1/15/2016'],
             'Template': 'Instrument.Derivative.BermudanOption'},
            {'AsOfDate': asof_date,
             'Basis': 'ACTUAL/365Fixed',
             'Calendar': 'UnitedStates',
             'DiscountRate': 0.001,
             'DividendRate': 0.0163,
             'ObjectId': 'BSMProcess',
             'Spot': 127.62,
             'Template': 'Process.Equity.BlackScholesMerton',
             'Volatility': 0.20},
            {'GeneralBlackScholesProcess': '->BSMProcess',
             'ObjectId': 'BermudanEngine',
             'Template': 'Engine.Equity.FdBermudan'}
        ]

        controller = Controller(data)
        controller.process(asof_date)
        option = controller.object("BermudanOption")
        npv = option.NPV()
        self.assertAlmostEqual(npv, 6.808761233089867)
