import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase


class DiscountingBondEngineCreator(CreatorBase):
    _templates = [T.ENGINE_BOND_DISCOUNTING]
    _req_fields = [F.DISCOUNT_CURVE]
    _opt_fields = []

    def _create(self, asof_date):
        discount_curve = self[F.DISCOUNT_CURVE]
        handle = ql.YieldTermStructureHandle(discount_curve)
        engine = ql.DiscountingBondEngine(handle)
        return engine

    @classmethod
    def set_info(cls):
        cls.desc("Creates a discounting bond engine to value bond cashflows")
        cls.field(F.DISCOUNT_CURVE, "The reference yield curve to use for discounting")


class AnalyticEuropeanEngineCreator(CreatorBase):
    _templates = [T.ENGINE_EQUITY_ANALYTICEUROPEAN]
    _req_fields = [F.GENERAL_BLACKSCHOLES_PROCESS]
    _opt_fields = []

    def _create(self, asof_date):
        process = self[F.GENERAL_BLACKSCHOLES_PROCESS]
        engine = ql.AnalyticEuropeanEngine(process)
        return engine

    @classmethod
    def set_info(cls):
        cls.desc("This template creates the analytic European engine to price European options.")
        cls.field(F.GENERAL_BLACKSCHOLES_PROCESS, "The generalized Black Scholes process.")


class FDAmericanEngineCreator(CreatorBase):
    _templates = [T.ENGINE_EQUITY_FDAMERICAN]
    _req_fields = [F.GENERAL_BLACKSCHOLES_PROCESS]
    _opt_fields = []

    def _create(self, asof_date):
        process = self[F.GENERAL_BLACKSCHOLES_PROCESS]
        engine = ql.FDAmericanEngine(process)
        return engine

    @classmethod
    def set_info(cls):
        cls.desc("This template creates the Finite Difference American engine to price American options.")
        cls.field(F.GENERAL_BLACKSCHOLES_PROCESS, "The generalized Black Scholes process.")


class FDBermudanEngineCreator(CreatorBase):
    _templates = [T.ENGINE_EQUITY_FDBERMUDAN]
    _req_fields = [F.GENERAL_BLACKSCHOLES_PROCESS]
    _opt_fields = []

    def _create(self, asof_date):
        process = self[F.GENERAL_BLACKSCHOLES_PROCESS]
        engine = ql.FDBermudanEngine(process)
        return engine

    @classmethod
    def set_info(cls):
        cls.desc("This template creates the Finite Difference Bermudan engine to price Bermudan options.")
        cls.field(F.GENERAL_BLACKSCHOLES_PROCESS, "The generalized Black Scholes process.")
