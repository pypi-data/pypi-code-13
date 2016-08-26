import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import InstrumentCreatorBase
from .utils import ScheduleCreator


class FixedRateBondCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_BOND_TBOND]
    _req_fields = [F.CURRENCY, F.ISSUE_DATE, F.MATURITY_DATE]
    _opt_fields = [F.ACCRUAL_CALENDAR, F.ACCRUAL_DAY_CONVENTION, F.TERMINATION_DAY_CONVENTION,
                    F.END_OF_MONTH, F.DATE_GENERATION, F.COUPON_FREQ, F.SETTLEMENT_DAYS, F.FACE_AMOUNT,
                    F.COUPON, F.LIST_OF_COUPONS, F.PAYMENT_CALENDAR, F.PAYMENT_DAY_CONVENTION,
                    F.REDEMPTION, F.EXCOUPON_PERIOD, F.EXCOUPON_CALENDAR, F.EXCOUPON_DAY_CONVENTION,
                    F.EXCOUPON_END_OF_MONTH, F.COMPOUNDING]

    def _create(self, asof_date):
        schedule = ScheduleCreator(self.data).create(asof_date)
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        issue_date = self[F.ISSUE_DATE]

        accrual_basis = self.get(F.ACCRUAL_BASIS)
        coupon_freq = self.get(F.COUPON_FREQ)
        compounding = self.get(F.COMPOUNDING)
        coupon = self.get(F.COUPON) or self.get(F.LIST_OF_COUPONS) or 0.0
        coupon = [coupon] if not isinstance(coupon, list) else coupon
        coupon = [ql.InterestRate(c, accrual_basis, compounding, coupon_freq) for c in coupon]
        pay_calendar = self.get(F.PAYMENT_CALENDAR) or self.get(F.ACCRUAL_CALENDAR)
        pay_convention = self.get(F.PAYMENT_DAY_CONVENTION) or self.get(F.ACCRUAL_DAY_CONVENTION)
        redemption = self.get(F.REDEMPTION, face_amount)
        excoupon_period = self.get(F.EXCOUPON_PERIOD, ql.Period())
        excoupon_calendar = self.get(F.EXCOUPON_CALENDAR) or pay_calendar
        excoupon_convention = self.get(F.EXCOUPON_DAY_CONVENTION, ql.Unadjusted)
        excoupon_end_of_month = self.get(F.EXCOUPON_END_OF_MONTH, False)

        bond = ql.FixedRateBond(
            settlement_days,
            face_amount,
            schedule,
            coupon,
            pay_convention,
            redemption,
            issue_date,
            pay_calendar,
            excoupon_period,
            excoupon_calendar,
            excoupon_convention,
            excoupon_end_of_month
        )
        return bond

    @classmethod
    def set_info(cls):
        cls.desc("A template for creating a Fixed Rate Bond.")


class ZeroCouponBondCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_BOND_TBILL]
    _req_fields = [F.ISSUE_DATE, F.MATURITY_DATE, F.CURRENCY]
    _opt_fields = [F.ASOF_DATE, F.SETTLEMENT_DAYS,
                   F.PAYMENT_CALENDAR, F.PAYMENT_DAY_CONVENTION, F.REDEMPTION,
                   F.FACE_AMOUNT]

    def _create(self, asof_date):
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        maturity_date = self.get(F.MATURITY_DATE)
        issue_date = self.get(F.ISSUE_DATE) or self.get(F.ASOF_DATE) or asof_date
        pay_calendar = self.get(F.PAYMENT_CALENDAR)
        pay_convention = self.get(F.PAYMENT_DAY_CONVENTION)
        redemption = self.get(F.REDEMPTION, face_amount)

        bond = ql.ZeroCouponBond(
            settlement_days,
            pay_calendar,
            face_amount,
            maturity_date,
            pay_convention,
            redemption,
            issue_date
        )
        return bond

    @classmethod
    def set_info(cls):
        cls.desc("A template for creating a Zero Coupon Bond.")


class CallableFixedRateBondCreator(InstrumentCreatorBase):
    _templates = []
    _req_fields = []
    _opt_fields = []

    def _create(self, asof_date):
        pass