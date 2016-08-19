import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase


class DiscountingBondEngineCreator(CreatorBase):
    _templates = [T.ENGINES_BOND_DISCOUNTING]
    _req_fields = [F.DISCOUNT_CURVE]
    _opt_fields = []

    def _create(self, asof_date):
        discount_curve = self[F.DISCOUNT_CURVE]
        handle = ql.YieldTermStructureHandle(discount_curve)
        engine = ql.DiscountingBondEngine(handle)
        return engine


