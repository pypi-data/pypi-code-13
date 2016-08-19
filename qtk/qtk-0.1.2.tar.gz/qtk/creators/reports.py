import QuantLib as ql
from qtk.templates import Template as T
from qtk.fields import Field as F
from .common import CreatorBase

class BondMarketReport(object):
    def __init__(self):
        self.clean_price = None
        self.modified_duration = None
        self.asof_date = None
        self.accrued_interest = None
        self.bond_yield = None



class BondMarketAnalyticsCreator(CreatorBase):
    _templates = [T.ANALYTICS_MARKET_BOND]
    _req_fields = [F.INSTRUMENT]
    _opt_fields = [F.PRICE, F.YIELD, F.PRICE_DIRTY, F.DISCOUNT_BASIS,
                   F.COMPOUNDING_FREQ, F.COMPOUNDING, F.YIELD_COMPOUNDING,
                   F.YIELD_COMPOUNDING_FREQ, F.ACCRUAL_BASIS]

    def _create(self, asof_date):
        bond = self[F.INSTRUMENT]
        assert isinstance(bond, ql.Bond) == True
        discount_curve = self[F.DISCOUNT_CURVE]
        assert isinstance(discount_curve, ql.YieldTermStructure)
        engine = ql.DiscountingBondEngine(discount_curve)
        bond.setPricingEngine(engine)
        asof_date = self[F.ASOF_DATE]
        yield_basis = self.get(F.DISCOUNT_BASIS, discount_curve.dayCounter())
        comp_freq = self.get(F.COMPOUNDING_FREQ, ql.Semiannual)
        compounding = self.get(F.COMPOUNDING, ql.Compounded)

        price = self.get(F.PRICE)
        if price is None:
            yld = self[F.YIELD]
            price = bond.cleanPrice()
        else:
            yld = bond.bondYield()
        """
        report.bond_yield = yld
        report.clean_price = ql.BondFunctions.cleanPrice(
        bond, yld, yield_basis, compounding, comp_freq, asof_date)
        else:
        price_dirty = self.get(F.PRICE_DIRTY, False)
        # TODO: handle the case of price being passed as dirty
        report.clean_price = price
        """


class MarketReportCreator(CreatorBase):
    _templates = [T.REPORTS_MARKET_ALL]
    _req_fields = [F.INSTRUMENT_COLLECTION, F.DISCOUNT_CURVE, F.ASOF_DATE]
    _opt_fields = [F.PRICE, F.YIELD, F.PRICE_DIRTY, F.DISCOUNT_BASIS,
                   F.COMPOUNDING_FREQ, F.COMPOUNDING]

    def _create(self, asof_date):
        report = BondMarketReport()
        instruments = self[F.INSTRUMENT_COLLECTION]  # list of dict
        for instrument_dict in instruments:
            if isinstance(instrument_dict, dict):
                obj = instrument_dict[F.OBJECT.id]
                assert isinstance(obj, ql.Bond) == True
                packet = self.data





        return report