import QuantLib as ql
from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase


class BlackConstantVolatilityCreator(CreatorBase):
    _templates = [T.TS_VOLATILITY_BLACKCONSTANT]
    _req_fields = [F.VOLATILITY, F.CALENDAR, F.BASIS, F.ASOF_DATE]
    _opt_fields = []

    def _create(self, asof_date):
        basis = self[F.BASIS]
        volatility = self[F.VOLATILITY]
        calendar = self[F.CALENDAR]
        asof_date = self[F.ASOF_DATE]
        vol = ql.BlackConstantVol(
            asof_date, calendar, ql.QuoteHandle(ql.SimpleQuote(volatility)), basis)
        return vol

    @classmethod
    def set_info(cls):
        cls.desc("This is a template for creating a constant Black volatility term structure.")


class BlackVolatilityCurveCreator(CreatorBase):
    _templates = [T.TS_VOLATILITY_BLACKCURVE]
    _req_fields = [F.LIST_OF_VOLATILITIES, F.LIST_OF_DATES, F.BASIS, F.ASOF_DATE]
    _opt_fields = []

    def _create(self, asof_date):
        basis = self[F.BASIS]
        volatilities = self[F.LIST_OF_VOLATILITIES]
        dates = self[F.LIST_OF_DATES]
        if len(dates) == len(volatilities):
            asof_date = self[F.ASOF_DATE]
            vol = ql.BlackVarianceCurve(
                    asof_date, dates, volatilities, basis)
            return vol
        else:
            raise ValueError("Sizes of volatility and date lists are not the same!")

    @classmethod
    def set_info(cls):
        cls.desc("This is a template for creating a Black volatility curve term structure.")


class BlackVolatilitySurfaceCreator(CreatorBase):
    _templates = [T.TS_VOLATILITY_BLACKSURFACE]
    _req_fields = [F.LIST_OF_LIST_OF_VOLATILITIES, F.LIST_OF_DATES, F.LIST_OF_STRIKES, F.CALENDAR, F.BASIS, F.ASOF_DATE]
    _opt_fields = []

    def _create(self, asof_date):
        list_list_vols = self[F.LIST_OF_LIST_OF_VOLATILITIES]
        ref_date = self[F.ASOF_DATE]
        calendar = self[F.CALENDAR]
        basis = self[F.BASIS]
        strikes = self[F.LIST_OF_STRIKES]
        dates = self[F.LIST_OF_DATES]
        implied_vols = ql.Matrix(len(strikes), len(dates))
        if (len(dates) == len(list_list_vols)):
            for i in range(implied_vols.rows()):
                for j in range(implied_vols.columns()):
                    implied_vols[i][j] = list_list_vols[j][i]
            vol_surface = ql.BlackVarianceSurface(ref_date, calendar, dates, strikes, implied_vols, basis)
            return vol_surface
        else:
            raise ValueError("The number of rows in vol matrix should be the size of dates")

    @classmethod
    def set_info(cls):
        cls.desc("This is a template for creating a Black volatility surface term structure.")
        cls.field(F.LIST_OF_LIST_OF_VOLATILITIES, "The list of list of volatilities, with each row for each expiration "
                                                  "date and each column for different strikes.")
