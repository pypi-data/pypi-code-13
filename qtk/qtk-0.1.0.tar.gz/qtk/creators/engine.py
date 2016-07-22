from .common import CreatorBase
from qtk.templates import Template as T
from qtk.fields import Field as F
import QuantLib as ql


class DiscountingBondEngineCreator(CreatorBase):
    _templates = [T.ENG_BOND_DISCOUNTING]
    _req_fields = [F.DISCOUNT_CURVE]
    _opt_fields = []

    def _create(self, asof_date):
        discount_curve = self.get(F.DISCOUNT_CURVE)
        handle = ql.YieldTermStructureHandle(discount_curve)
        engine = ql.DiscountingBondEngine(handle)
        return engine


