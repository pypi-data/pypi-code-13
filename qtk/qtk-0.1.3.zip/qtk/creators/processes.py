import QuantLib as ql
from qtk.templates import Template as T
from qtk.fields import Field as F
from .common import CreatorBase


class BlackScholesMertonProcess(CreatorBase):
    _templates = [T.PROCESS_EQUITY_BLACKSCHOLESMERTON]
    _req_fields = [F.SPOT]
    _opt_fields = [F.ASOF_DATE, F.DIVIDEND_YIELD, F.DIVIDEND_RATE, F.DISCOUNT_CURVE, F.DISCOUNT_RATE,
                   F.BLACKVOLATILITY_TERMSTRUCTURE, F.CALENDAR, F.VOLATILITY, F.BASIS]

    def _create(self, asof_date):
        spot = self[F.SPOT]
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
        asof_date = self.get(F.ASOF_DATE, asof_date)
        divyield = self.get(F.DIVIDEND_YIELD)
        basis = self.get(F.BASIS, ql.ActualActual())
        if divyield is None:
            divrate = self.get(F.DIVIDEND_RATE, 0.0)
            divyield = ql.FlatForward(asof_date, divrate, basis)
        div_handle = ql.YieldTermStructureHandle(divyield)
        discyield = self.get(F.DISCOUNT_CURVE)
        if discyield is None:
            discrate = self[F.DISCOUNT_RATE]
            discyield = ql.FlatForward(asof_date, discrate, basis)
        disc_handle = ql.YieldTermStructureHandle(discyield)
        vol_ts = self.get(F.BLACKVOLATILITY_TERMSTRUCTURE)
        if vol_ts is None:
            calendar = self[F.CALENDAR]
            volrate = self[F.VOLATILITY]
            vol_ts = ql.BlackConstantVol(asof_date, calendar, volrate, basis)
        vol_handle = ql.BlackVolTermStructureHandle(vol_ts)
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, div_handle, disc_handle, vol_handle)
        return bsm_process

    @classmethod
    def set_info(cls):
        cls.desc("This template creates the Black Scholes Merton process.")
        cls.field(F.DIVIDEND_YIELD,
                  "The yield term structure for dividend. If not given, a flat yield term structure is created using "
                  "the value for %s." % F.DISCOUNT_RATE.id)
        cls.field(F.DIVIDEND_RATE,
                  "The dividend rate for creating a flat dividend yield term structure. If both %s and %s are not "
                  "provided, then a 0.0 dividend rate is assumed." % (F.DIVIDEND_RATE.id, F.DIVIDEND_YIELD.id))
        cls.field(F.DISCOUNT_CURVE,
                  "The interest rate term structure for discounting cashflows. If not provided, one would need to "
                  "provide %s." % F.DISCOUNT_RATE.id)
        cls.field(F.DISCOUNT_RATE,
                  "The risk free interest rate used to construct a flat term structure. Used only when %s is not "
                  "provided." % F.DISCOUNT_CURVE.id)
        cls.field(F.BLACKVOLATILITY_TERMSTRUCTURE,
                  "The Black volatility term structure, either as constant vol, black volatility curve, or Black "
                  "volatility surface. If this is not provided, the value given by %s is used to construct a "
                  "constant Black volatility surface." % F.VOLATILITY.id)
        cls.field(F.CALENDAR, "The calendar is needed if %s is not provided and %s is what is used instead." %
                  (F.BLACKVOLATILITY_TERMSTRUCTURE.id, F.VOLATILITY))
        cls.field(F.BASIS, "If basis is not provided, the ActualActual day count is assumed.")
