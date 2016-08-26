import QuantLib as ql
from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import InstrumentCreatorBase


class EuropeanOptionCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_DERIVATIVE_EUROPEANOPTION]
    _req_fields = [F.STRIKE, F.OPTION_TYPE, F.MATURITY_DATE]
    _opt_fields = []

    def _create(self, asof_date):
        strike_price = self[F.STRIKE]
        option_type = self[F.OPTION_TYPE]
        maturity_date = self[F.MATURITY_DATE]

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.EuropeanExercise(maturity_date)
        european_option = ql.VanillaOption(payoff, exercise)
        return european_option


class AmericanOptionCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_DERIVATIVE_AMERICANOPTION]
    _req_fields = [F.STRIKE, F.OPTION_TYPE, F.MATURITY_DATE]
    _opt_fields = [F.START_DATE, F.PAYOFF_AT_EXPIRY]

    def _create(self, asof_date):
        strike_price = self[F.STRIKE]
        option_type = self[F.OPTION_TYPE]
        maturity_date = self[F.MATURITY_DATE]
        start_date = self.get(F.START_DATE, asof_date)
        payoff_at_expiry = self.get(F.PAYOFF_AT_EXPIRY, False)

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.AmericanExercise(start_date, maturity_date, payoff_at_expiry)
        american_option = ql.VanillaOption(payoff, exercise)
        return american_option

    @classmethod
    def set_info(cls):
        cls.desc("This is a template for creating an American style option")
        cls.field(F.START_DATE,"Exercise start date. If not given, starts on asof date.")


class BermudanOptionCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_DERIVATIVE_BERMUDANOPTION]
    _req_fields = [F.STRIKE, F.OPTION_TYPE, F.LIST_OF_DATES]
    _opt_fields = [F.ASOF_DATE]

    def _create(self, asof_date):
        strike_price = self[F.STRIKE]
        option_type = self[F.OPTION_TYPE]
        exercise_dates = self.get(F.LIST_OF_DATES)
        payoff_at_expiry = self.get(F.PAYOFF_AT_EXPIRY, False)

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.BermudanExercise(exercise_dates, payoff_at_expiry)
        bermudan_option = ql.VanillaOption(payoff, exercise)
        return bermudan_option
