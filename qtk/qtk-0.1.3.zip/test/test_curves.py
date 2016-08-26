import QuantLib as ql
from unittest import TestCase
from qtk import Controller, Field as F, QuantLibConverter as qlc, Template as T

import copy


_bond_sample_data = {
    'AsOfDate': '2016-06-14',
    'Country': 'US',
    'Currency': 'USD',
    'DataSource': 'TEST',
    "ObjectId": "Curve",
    'InstrumentCollection': [{'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-01-07',
                              'MaturityDate': '2016-07-07',
                              'Yield': '0.00212500',
                              'SecurityId': '912796HZ Govt',
                              'Template': T.INSTRUMENT_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2015-09-17',
                              'MaturityDate': '2016-09-15',
                              'Yield': '0.002625',
                              'SecurityId': '912796HE Govt',
                              'Template': T.INSTRUMENT_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-06-16',
                              'MaturityDate': '2016-12-15',
                              'Yield': '0.003925',
                              'SecurityId': '912796JY Govt',
                              'Template': T.INSTRUMENT_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-05-26',
                              'MaturityDate': '2017-05-25',
                              'Yield': '0.005300',
                              'SecurityId': '912796JT Govt',
                              'Template': T.INSTRUMENT_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.008750',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2018-05-31',
                              'Price': '100.292969',
                              'SecurityId': '912828R5 Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.008750',
                              'Currency': 'USD',
                              'IssueDate': '2016-06-15',
                              'MaturityDate': '2019-06-15',
                              'Price': '100.066406',
                              'SecurityId': '912828R8 Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.013750',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2021-05-31',
                              'Price': '101.136719',
                              'SecurityId': '912828R7 Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.016250',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2023-05-31',
                              'Price': '101.382813',
                              'SecurityId': '912828R6 Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.016250',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-16',
                              'MaturityDate': '2026-05-15',
                              'Price': '100.101563',
                              'SecurityId': '912828R3 Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.025000',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-16',
                              'MaturityDate': '2046-05-15',
                              'Price': '101.617188',
                              'SecurityId': '912810RS Govt',
                              'Template': T.INSTRUMENT_BOND_TBOND_HELPER.id}],
    'Template': 'TermStructure.Yield.BondCurve'
}


class TestCurves(TestCase):

    def setUp(self):
        self._bond_data = copy.deepcopy(_bond_sample_data)

    def test_us_bond_curve(self):
        res = Controller([self._bond_data])
        asof_date = qlc.to_date(self._bond_data[F.ASOF_DATE.id])

        res.process(asof_date)
        curve = res.object("Curve")
        self.assertIsInstance(curve, ql.YieldTermStructure)

        tenors = range(0,13,1) + [60, 90, 120, 240, 300, 359, 360]
        # reference
        vals = [1,0.999818753,0.999586047,0.999330996,0.998969924,0.998519955,0.998012046,
                0.997480698,0.996973715,0.996446467,0.995819544,0.995147323,0.994527808,
                0.94416047,0.895823056,0.848952274,0.654149304,0.553888921,0.459284189,
                0.458072534]
        # last observed
        vals = [1.0, 0.9998187481880838, 0.9995860408491943, 0.9993309911166345, 0.998969919388518, 0.9985199520192828,
         0.9980120452385237, 0.9974638785194306, 0.9969737149981466, 0.9964464679686021, 0.9957564702629885,
         0.9951473260058783, 0.9945282870008731, 0.9440478657964286, 0.8958540539792529, 0.8489512443374962,
         0.6541478087480587, 0.553887387818232, 0.45928271508412133, 0.45770699043771784]

        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        for i, t in enumerate(tenors):
            p = ql.Period(t, ql.Months)
            d = calendar.advance(asof_date, ql.Period(t, ql.Months),ql.ModifiedFollowing)
            o = curve.discount(d)
            v = vals[i]
            self.assertAlmostEqual(o, v, 15, msg="("+str(t)+","+str(d)+","+str(o)+","+str(v)+")")
            #print t, d, o, v

    def test_zero_curve(self):
        data = {
            "ListOfDate": ["7/5/2016", "8/1/2016", "9/1/2016", "10/1/2016"],
            "ListOfZeroRate": [0.0, 0.001,0.002, 0.003],
            "DiscountBasis": "30/360",
            'Template': 'TermStructure.Yield.ZeroCurve',
            "Currency": "USD",
            "ObjectId": "Curve",
            "DiscountCalendar": "UnitedStates.GovernmentBond"

        }
        res = Controller([data])
        asof_date = qlc.to_date("7/5/2016")

        ret = res.process(asof_date)
        zcurve = res.object("Curve")
        data2 = res.object_data("Curve")
        observed = [zcurve.discount(d) for d in data2["ListOfDate"]]
        expected = [1.0, 0.9999277803857397, 0.9996889372789323, 0.9992835900775519]
        self.assertListEqual(observed, expected)

    def test_discount_curve(self):
        data = {
            "ListOfDate": ["7/5/2016", "8/1/2016", "9/1/2016", "10/1/2016"],
            "ListOfDiscountFactor": [1.0, 0.99, 0.98, 0.97],
            "DiscountBasis": "30/360",
            'Template': 'TermStructure.Yield.DiscountCurve',
            "Currency": "USD",
            "ObjectId": "Curve",
            "DiscountCalendar": "UnitedStates.GovernmentBond"
        }

        res = Controller([data])
        asof_date = qlc.to_date("7/5/2016")
        res.process(asof_date)
        dcurve = res.object("Curve")
        data2 = res.object_data("Curve")
        observed = [dcurve.discount(d) for d in data2["ListOfDate"]]
        expected = data["ListOfDiscountFactor"]
        self.assertListEqual(observed, expected)

    def test_flat_forward(self):
        asof_date = "7/22/2016"
        data = [{
            F.FORWARD_RATE.id: 0.01,
            F.ASOF_DATE.id: asof_date,
            F.DISCOUNT_BASIS.id: "30/360",
            F.CURRENCY.id: "USD",
            F.OBJECT_ID.id: "USD.Flat.Curve",
            F.TEMPLATE.id: T.TS_YIELD_FLAT
        }]

        res = Controller(data)
        res.process(asof_date)
        curve = res.object("USD.Flat.Curve")
        observed = [curve.discount(d) for d in [0.0, 0.25, 0.5, 1.0]]
        expected = [1.0, 0.99750312239746, 0.9950124791926824, 0.9900498337491681]
        self.assertListEqual(observed, expected)



