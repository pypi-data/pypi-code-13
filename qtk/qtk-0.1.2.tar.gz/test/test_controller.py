from unittest import TestCase
from qtk.templates import Template as T
import copy
from qtk import Controller, Field, QuantLibConverter as qlc
import QuantLib as ql

_bond_sample_data = [
    {
    'AsOfDate': '2016-06-14',
    'Country': 'US',
    'Currency': 'USD',
    'DataSource': 'TEST',
    'InstrumentCollection': [{'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-01-07',
                              'MaturityDate': '2016-07-07',
                              'Yield': '0.00212500',
                              'SecurityId': '912796HZ Govt',
                              'ObjectId': 'Inst21',
                              'Template': T.INST_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2015-09-17',
                              'MaturityDate': '2016-09-15',
                              'Yield': '0.002625',
                              'SecurityId': '912796HE Govt',
                              'ObjectId': 'Inst22',
                              'Template': T.INST_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-06-16',
                              'MaturityDate': '2016-12-15',
                              'Yield': '0.003925',
                              'SecurityId': '912796JY Govt',
                              'ObjectId': 'Inst23',
                              'Template': T.INST_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.000000',
                              'CouponFrequency': None,
                              'Currency': 'USD',
                              'AccrualBasis': 'ACT/360',
                              'IssueDate': '2016-05-26',
                              'MaturityDate': '2017-05-25',
                              'Yield': '0.005300',
                              'SecurityId': '912796JT Govt',
                              'ObjectId': 'Inst24',
                              'Template': T.INST_BOND_TBILL_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.008750',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2018-05-31',
                              'Price': '100.292969',
                              'SecurityId': '912828R5 Govt',
                              'ObjectId': 'Inst25',
                              'Template': T.INST_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.008750',
                              'Currency': 'USD',
                              'IssueDate': '2016-06-15',
                              'MaturityDate': '2019-06-15',
                              'Price': '100.066406',
                              'SecurityId': '912828R8 Govt',
                              'ObjectId': 'Inst26',
                              'Template': T.INST_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.013750',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2021-05-31',
                              'Price': '101.136719',
                              'SecurityId': '912828R7 Govt',
                              'ObjectId': 'Inst27',
                              'Template': T.INST_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.016250',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-31',
                              'MaturityDate': '2023-05-31',
                              'Price': '101.382813',
                              'SecurityId': '912828R6 Govt',
                              'ObjectId': 'Inst28',
                              'Template': T.INST_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.016250',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-16',
                              'MaturityDate': '2026-05-15',
                              'Price': '100.101563',
                              'SecurityId': '912828R3 Govt',
                              'ObjectId': 'Inst29',
                              'Template': T.INST_BOND_TBOND_HELPER.id},
                             {'AsOfDate': '2016-06-14',
                              'Coupon': '0.025000',
                              'Currency': 'USD',
                              'IssueDate': '2016-05-16',
                              'MaturityDate': '2046-05-15',
                              'Price': '101.617188',
                              'SecurityId': '912810RS Govt',
                              'ObjectId': 'Inst210',
                              'Template': T.INST_BOND_TBOND_HELPER.id}],
    'Template': 'TermStructure.Yield.BondCurve',
    "ObjectId": "USD.Bond.Curve"},
    {'AsOfDate': '2016-06-14',
     'Coupon': '0.000000',
     'CouponFrequency': None,
     'Currency': 'USD',
     'AccrualBasis': 'ACT/360',
     'IssueDate': '2016-01-07',
     'MaturityDate': '2016-07-07',
     'Yield': '0.00212500',
     'SecurityId': '912796HZ Govt',
     'ObjectId': 'Inst1',
     "PricingEngine": "->BondEngine",
     'Template': T.INST_BOND_TBILL.id},
    {'AsOfDate': '2016-06-14',
     'Coupon': '0.000000',
     'CouponFrequency': None,
     'Currency': 'USD',
     'AccrualBasis': 'ACT/360',
     'IssueDate': '2015-09-17',
     'MaturityDate': '2016-09-15',
     'Yield': '0.002625',
     'SecurityId': '912796HE Govt',
     'ObjectId': 'Inst2',
     "PricingEngine": "->BondEngine",
     'Template': T.INST_BOND_TBILL.id},
    {'AsOfDate': '2016-06-14',
     'Coupon': '0.000000',
     'CouponFrequency': None,
     'Currency': 'USD',
     'AccrualBasis': 'ACT/360',
     'IssueDate': '2016-06-16',
     'MaturityDate': '2016-12-15',
     'Yield': '0.003925',
     'SecurityId': '912796JY Govt',
     'ObjectId': 'Inst3',
     "PricingEngine": "->BondEngine",
     'Template': T.INST_BOND_TBILL.id},
    {'DiscountCurve': "->USD.Bond.Curve",
     "ObjectId": "BondEngine",
     "Template": T.ENGINES_BOND_DISCOUNTING.id}
    ]


class TestController(TestCase):

    def setUp(self):
        self._bond_data = _bond_sample_data

    def test_graph_dependency(self):
        res = Controller(self._bond_data)
        asof_date = qlc.to_date(self._bond_data[0][Field.ASOF_DATE.id])

        res.process(asof_date)
        curve = res.object("USD.Bond.Curve")
        self.assertIsInstance(curve, ql.YieldTermStructure)
        bond = res.object("Inst1")
        price = bond.cleanPrice()
        self.assertEqual(price, 99.98642361111114)
        return

    def test_duplicate_id_error(self):
        data = self._bond_data + [self._bond_data[-1]]
        error = ""
        try:
            res = Controller(data)
            asof_date = qlc.to_date(self._bond_data[0][Field.ASOF_DATE.id])
            res.process(asof_date)
        except ValueError as e:
            error = e.message

        self.assertEqual(error, 'Duplicate ObjectId BondEngine found')
        return

    def test_dependency_cycles_err(self):
        data = copy.deepcopy(self._bond_data)
        data[-1]['DiscountCurve'] = "->Inst2"
        error = ""
        try:
            res = Controller(data)
            asof_date = qlc.to_date(self._bond_data[0][Field.ASOF_DATE.id])
            res.process(asof_date)
        except ValueError as e:
            error = e.message

        self.assertEqual(error, "Found cycles in dependencies [['Inst2', 'BondEngine']]")
        return

    def test_datatype_check_err(self):
        data = copy.deepcopy(self._bond_data)
        data[-2]['PricingEngine'] = "->USD.Bond.Curve"
        error = ""
        try:
            res = Controller(data)
            asof_date = qlc.to_date(self._bond_data[0][Field.ASOF_DATE.id])
            res.process(asof_date)
        except ValueError as e:
            error = e.message

        self.assertEqual(error, 'Incompatible data type for field PricingEngine in object Inst3')
        return

    def test_context(self):
        curve_data = [self._bond_data[0]]
        rest_data = self._bond_data[1:]
        res = Controller(curve_data)
        asof_date = qlc.to_date(self._bond_data[0][Field.ASOF_DATE.id])
        res.process(asof_date)
        context = res.data

        res = Controller(rest_data, context=context)
        res.process(asof_date)
        bond = res.object("Inst1")
        price = bond.cleanPrice()
        self.assertEqual(price, 99.98642361111114)
        return