import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase


class ScheduleCreator(CreatorBase):
    _templates = [T.TIME_MAIN_SCHEDULE]
    _req_fields = [F.ISSUE_DATE, F.MATURITY_DATE, F.ACCRUAL_CALENDAR,
                   F.ACCRUAL_DAY_CONVENTION]
    _opt_fields = [F.TERMINATION_DAY_CONVENTION, F.END_OF_MONTH, F.DATE_GENERATION, F.COUPON_FREQ]

    def _create(self, asof_date):
        maturity_date = self[F.MATURITY_DATE]
        issue_date = self.get(F.ISSUE_DATE) or self.get(F.ASOF_DATE) or asof_date
        coupon_freq = self.get(F.COUPON_FREQ)
        period = ql.Period(coupon_freq)
        calendar = self.get(F.ACCRUAL_CALENDAR)
        convention = self.get(F.ACCRUAL_DAY_CONVENTION)
        termination_convention = self.get(F.TERMINATION_DAY_CONVENTION, convention)
        end_of_month = self.get(F.END_OF_MONTH, True)
        rule = self.get(F.DATE_GENERATION, ql.DateGeneration.Backward)

        schedule = ql.Schedule(issue_date,
                               maturity_date,
                               period,
                               calendar,
                               convention,
                               termination_convention,
                               rule,
                               end_of_month)
        return schedule