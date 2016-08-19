import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase
from .utils import ScheduleCreator


class DepositRateHelperCreator(CreatorBase):
    _templates = [T.INST_BOND_TBILL_HELPER]
    _req_fields = [F.ISSUE_DATE, F.MATURITY_DATE, F.COUPON, F.CURRENCY]
    _opt_fields = [F.PRICE, F.YIELD]

    def _bond_schedule(self):
        maturity_date = self.get(F.MATURITY_DATE)
        asof_date = self.get(F.ASOF_DATE)
        period = ql.Period(1, ql.Years)
        calendar = self.get(F.ACCRUAL_CALENDAR)
        convention = self.get(F.ACCRUAL_DAY_CONVENTION)
        termination_convention = self.get(F.TERMINATION_DAY_CONVENTION, convention)
        end_of_month = self.get(F.END_OF_MONTH, True)

        schedule = ql.Schedule(asof_date,
                               maturity_date,
                               period,
                               calendar,
                               convention,
                               termination_convention,
                               ql.DateGeneration.Backward,
                               end_of_month)
        return schedule

    def _create(self, asof_date):
        schedule = self._bond_schedule()
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        day_count = self.get(F.ACCRUAL_BASIS)
        convention = self.get(F.ACCRUAL_DAY_CONVENTION)
        maturity_date = self.get(F.MATURITY_DATE)
        asof_date = self.get(F.ASOF_DATE)

        price = self.get(F.PRICE)
        rate = self.get(F.YIELD)
        if (price is None) and (rate is not None):
            price = face_amount*(1.0 - rate*day_count.yearFraction(asof_date, maturity_date))

        coupon = 0.0
        bond_helper = ql.FixedRateBondHelper(
            ql.QuoteHandle(ql.SimpleQuote(price)),
            settlement_days,
            face_amount,
            schedule,
            [coupon],
            day_count,
            convention
        )
        return bond_helper

    def _create_deporates(self, asof_date):
        rate = self.get(F.YIELD)
        maturity_date = self.get(F.MATURITY_DATE)

        settlement_days = self.get(F.SETTLEMENT_DAYS)
        day_count = self.get(F.ACCRUAL_BASIS)
        convention = self.get(F.ACCRUAL_DAY_CONVENTION)
        calendar = self.get(F.ACCRUAL_CALENDAR)
        days = day_count.dayCount(asof_date, maturity_date)
        tenor = ql.Period(days, ql.Days)
        end_of_month = self.get(F.END_OF_MONTH)

        depo_rate_helper = ql.DepositRateHelper(
            ql.QuoteHandle(ql.SimpleQuote(rate)),
            tenor,
            settlement_days,
            calendar,
            convention,
            end_of_month,
            day_count
        )
        return depo_rate_helper


class BondRateHelperCreator(CreatorBase):
    _templates = [T.INST_BOND_TBOND_HELPER]
    _req_fields = [F.ISSUE_DATE, F.MATURITY_DATE, F.COUPON, F.PRICE, F.CURRENCY]
    _opt_fields = [F.COUPON_FREQ]

    def _create(self, asof_date):
        schedule = ScheduleCreator(self.data).create(asof_date)
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        pay_basis = self.get(F.PAYMENT_BASIS) or self.get(F.ACCRUAL_BASIS)
        pay_convention = self.get(F.PAYMENT_DAY_CONVENTION) or self.get(F.ACCRUAL_DAY_CONVENTION)
        accrual_convention = self.get(F.ACCRUAL_DAY_CONVENTION)
        price = self.get(F.PRICE)
        coupon = self.get(F.COUPON)
        pay_calendar = self.get(F.PAYMENT_CALENDAR) or self.get(F.ACCRUAL_CALENDAR)
        dirty_price = self.get(F.PRICE_DIRTY, True)
        bond_helper = ql.FixedRateBondHelper(
            ql.QuoteHandle(ql.SimpleQuote(price)),
            settlement_days,
            face_amount,
            schedule,
            [coupon],
            pay_basis,
            pay_convention,
            face_amount,
            ql.Date(),
            pay_calendar,
            ql.Period(),
            pay_calendar,
            pay_convention,
            False,
            dirty_price
        )
        return bond_helper


class BondYieldCurveCreator(CreatorBase):
    # required fields
    _templates = [T.TS_YIELD_BOND]
    _req_fields = [F.INSTRUMENT_COLLECTION, F.ASOF_DATE, F.COUNTRY, F.CURRENCY]
    _opt_fields = [F.INTERPOLATION_METHOD, F.DISCOUNT_BASIS, F.SETTLEMENT_DAYS, F.DISCOUNT_CALENDAR]
    _values = {F.INTERPOLATION_METHOD.id: ["LinearZero", "CubicZero", "FlatForward",
                                            "LinearForward", "LogCubicDiscount"]}

    # class data
    _interpolator_map = {
        "LinearZero": ql.PiecewiseLinearZero,
        "CubicZero": ql.PiecewiseCubicZero,
        "FlatForward": ql.PiecewiseFlatForward,
        "LinearForward": ql.PiecewiseLinearForward,
        "LogCubicDiscount": ql.PiecewiseLogCubicDiscount
    }

    def _create(self, asof_date):
        curve_members = self.get(F.INSTRUMENT_COLLECTION)
        if curve_members:
            intepolator = self.get(F.INTERPOLATION_METHOD, "LinearZero")
            rate_helpers = [c[F.OBJECT.id] for c in curve_members]

            day_count = self.get(F.DISCOUNT_BASIS)

            yc_method = self._interpolator_map[intepolator]
            yc_curve = yc_method(
                asof_date, rate_helpers,
                day_count, [], []
            )
            yc_curve.enableExtrapolation()
            return yc_curve
        else:
            raise KeyError("Missing elements for key "+F.INSTRUMENT_COLLECTION.id)


class ZeroCurveCreator(CreatorBase):
    _templates = [T.TS_YIELD_ZERO]
    _req_fields = [F.LIST_OF_DATES, F.LIST_OF_ZERO_RATES, F.DISCOUNT_BASIS, F.DISCOUNT_CALENDAR]
    _opt_fields = [F.COMPOUNDING, F.COMPOUNDING_FREQ, F.EXTRAPOLATION]

    def _create(self, asof_date):
        dates = self.get(F.LIST_OF_DATES)
        zero_rates = self.get(F.LIST_OF_ZERO_RATES)
        discount_basis = self.get(F.DISCOUNT_BASIS)

        discount_calendar = self.get(F.DISCOUNT_CALENDAR)
        compounding = self.get(F.COMPOUNDING, ql.Continuous)
        frequency = self.get(F.COMPOUNDING_FREQ, ql.Annual)

        zero_curve = ql.ZeroCurve(dates, zero_rates, discount_basis, discount_calendar,
                                  ql.Linear(), compounding, frequency)
        if self.get(F.EXTRAPOLATION, True):
            zero_curve.enableExtrapolation()
        return zero_curve


class DiscountCurveCreator(CreatorBase):
    _templates = [T.TS_YIELD_DISCOUNT]
    _req_fields = [F.LIST_OF_DATES, F.LIST_OF_DISCOUNT_FACTORS, F.DISCOUNT_BASIS, F.DISCOUNT_CALENDAR]
    _opt_fields = []

    def _create(self, asof_date):
        dates = self.get(F.LIST_OF_DATES)
        discount_factors = self.get(F.LIST_OF_DISCOUNT_FACTORS)
        discount_basis = self.get(F.DISCOUNT_BASIS)
        discount_calendar = self.get(F.DISCOUNT_CALENDAR)
        discount_curve = ql.DiscountCurve(dates, discount_factors,
                                          discount_basis, discount_calendar)
        return discount_curve


class FlatForwardCurveCreator(CreatorBase):
    _templates = [T.TS_YIELD_FLAT]
    _req_fields = [F.FORWARD_RATE, F.DISCOUNT_BASIS]
    _opt_fields = [F.ASOF_DATE, F.SETTLEMENT_DAYS, F.SETTLEMENT_CALENDAR, F.COMPOUNDING, F.COMPOUNDING_FREQ]

    def _create(self, asof_date):
        basis = self[F.DISCOUNT_BASIS]
        compounding = self.get(F.COMPOUNDING, ql.Continuous)
        compound_freq = self.get(F.COMPOUNDING_FREQ, ql.Annual)
        forward = self[F.FORWARD_RATE]
        forward_quote = ql.QuoteHandle(ql.SimpleQuote(forward))
        asof_date = self.get(F.ASOF_DATE)
        if asof_date is None:
            settle_days = self.get(F.SETTLEMENT_DAYS)
            calendar = self.get(F.SETTLEMENT_CALENDAR)
            return ql.FlatForward(
                settle_days,
                calendar,
                forward_quote,
                basis,
                compounding,
                compound_freq
            )
        else:
            return ql.FlatForward(
                asof_date,
                forward_quote,
                basis,
                compounding,
                compound_freq
            )
