import QuantLib as ql
from .common import CreatorBase
from qtk.templates import Template as T
from qtk.fields import Field as F


class USDLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_USDLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.USDLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "USD"}


class CADLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_CADLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.CADLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "CAD"}


class GBPLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_GBPLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.GBPLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "GBP"}


class AUDLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_AUDLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.AUDLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "AUD"}


class JPYLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_JPYLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.JPYLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "JPY"}


class EURLiborCreator(CreatorBase):
    _templates = [T.INDEXES_IBOR_EURLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.EURLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "EUR"}
