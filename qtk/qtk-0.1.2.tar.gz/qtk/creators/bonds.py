import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase
from .utils import ScheduleCreator


# Fill the req and opt fields properly
class _BondCreator(CreatorBase):
    _base = True

    def create(self, asof_date):
        super(_BondCreator, self).create(asof_date)
        engine = self.get(F.PRICING_ENGINE)
        if engine:
            self._object.setPricingEngine(engine)
        return self._object


class FixedRateBondCreator(_BondCreator):
    _templates = [T.INST_BOND_TBOND]
    _req_fields = ScheduleCreator._req_fields
    _opt_fields = []

    def _create(self, asof_date):
        schedule = ScheduleCreator(self.data).create(asof_date)
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        coupon = self.get(F.COUPON) or self.get(F.LIST_OF_COUPONS) or 0.0
        coupon = [coupon] if not isinstance(coupon, list) else coupon
        issue_date = self.get(F.ISSUE_DATE) or self.get(F.ASOF_DATE) or asof_date
        pay_calendar = self.get(F.PAYMENT_CALENDAR) or self.get(F.ACCRUAL_CALENDAR)
        pay_basis = self.get(F.PAYMENT_BASIS) or self.get(F.ACCRUAL_BASIS)
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
            pay_basis,
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


class ZeroCouponBondCreator(_BondCreator):
    _templates = [T.INST_BOND_TBILL]
    _req_fields = [F.ISSUE_DATE, F.MATURITY_DATE]
    _opt_fields = [F.ASOF_DATE, F.SETTLEMENT_DAYS, F.MATURITY_DATE,
                   F.PAYMENT_CALENDAR, F.PAYMENT_DAY_CONVENTION, F.REDEMPTION]

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


