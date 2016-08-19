import QuantLib as ql
from unittest import TestCase
from qtk import Controller, Field as F, QuantLibConverter as qlc, Template as T


class TestIndexes(TestCase):

    def test_usd_libor(self):
        asof_date = "8/15/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "USD",
                F.OBJECT_ID.id: "USD.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_USDLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "USDLibor3M",
                F.YIELD_CURVE.id: "->USD.Flat.Curve"
            }
        ]
        res = Controller(data)
        res.process(asof_date)
        index = res.object("USDLibor3M")
        self.assertIsInstance(index, ql.USDLibor)

    def test_cad_libor(self):
        asof_date = "8/15/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "CAD",
                F.OBJECT_ID.id: "CAD.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_CADLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "CADLibor3M",
                F.YIELD_CURVE.id: "->CAD.Flat.Curve"
            }
        ]
        res = Controller(data)
        res.process(asof_date)
        index = res.object("CADLibor3M")
        self.assertIsInstance(index, ql.CADLibor)


    def test_jpy_libor(self):
        asof_date = "8/15/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "JPY",
                F.OBJECT_ID.id: "JPY.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_JPYLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "JPYLibor3M",
                F.YIELD_CURVE.id: "->JPY.Flat.Curve"
            }
        ]
        res = Controller(data)
        res.process(asof_date)
        index = res.object("JPYLibor3M")
        self.assertIsInstance(index, ql.JPYLibor)


    def test_gbp_libor(self):
        asof_date = "8/15/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "GBP",
                F.OBJECT_ID.id: "GBP.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_GBPLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "GBPLibor3M",
                F.YIELD_CURVE.id: "->GBP.Flat.Curve"
            }
        ]
        res = Controller(data)
        res.process(asof_date)
        index = res.object("GBPLibor3M")
        self.assertIsInstance(index, ql.GBPLibor)

    def test_eur_libor(self):
        asof_date = "8/15/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "EUR",
                F.OBJECT_ID.id: "EUR.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_EURLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "EURLibor3M",
                F.YIELD_CURVE.id: "->EUR.Flat.Curve"
            }
        ]
        res = Controller(data)
        res.process(asof_date)
        index = res.object("EURLibor3M")
        self.assertIsInstance(index, ql.EURLibor)