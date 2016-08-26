import QuantLib as ql
from .common import CreatorBase
from qtk.templates import Template as T
from qtk.fields import Field as F


class USDLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_USDLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.USDLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "USD"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates USD LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")


class CADLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_CADLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.CADLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "CAD"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates CAD LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")


class GBPLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_GBPLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.GBPLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "GBP"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates GBP LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")


class AUDLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_AUDLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.AUDLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "AUD"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates AUD LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")


class JPYLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_JPYLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.JPYLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "JPY"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates JPY LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")


class EURLiborCreator(CreatorBase):
    _templates = [T.INDEX_IBOR_EURLIBOR]
    _req_fields = [F.YIELD_CURVE, F.TENOR]
    _opt_fields = []

    def _create(self, asof_date):
        yield_curve = self[F.YIELD_CURVE]
        tenor = self[F.TENOR]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        return ql.EURLibor(tenor, yield_handle)

    def defaults(self):
        return {F.CURRENCY.id: "EUR"}

    @classmethod
    def set_info(cls):
        cls.desc("Creates EUR LIBOR index")
        cls.field(F.YIELD_CURVE, "The reference yield curve")
        cls.field(F.TENOR, "The reference tenor of the index")