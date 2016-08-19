import datetime

import QuantLib as ql
from dateutil.parser import parse


class QuantLibConverter(object):
    _daycount_map = {
        "ACT/ACT": ql.ActualActual(),
        "ACTUAL/ACTUAL": ql.ActualActual(),
        "ACT/365": ql.ActualActual(),  # Per ISDA
        "ACTUAL/ACTUALBOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACT/ACTBOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACTUAL/ACTUALEURO": ql.ActualActual(ql.ActualActual.Euro),
        "ACT/ACTEURO": ql.ActualActual(ql.ActualActual.Euro),

        "ACTUAL/365BOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACT/365BOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACTUAL/365EURO": ql.ActualActual(ql.ActualActual.Euro),
        "ACT/365EURO": ql.ActualActual(ql.ActualActual.Euro),

        "ACT/360": ql.Actual360(),
        "ACTUAL/360": ql.Actual360(),
        "A/360": ql.Actual360(),

        "30/360": ql.Thirty360(ql.Thirty360.USA),
        "360/360": ql.Thirty360(ql.Thirty360.USA),
        "BONDBASIS": ql.Thirty360(ql.Thirty360.USA),
        "30E/360": ql.Thirty360(ql.Thirty360.EurobondBasis),
        "EUROBONDBASIS": ql.Thirty360(ql.Thirty360.EurobondBasis),
        "30/360ITALIAN": ql.Thirty360(ql.Thirty360.Italian),

        "ACTUAL/365FIXED": ql.Actual365Fixed(),
        "ACT/365FIXED": ql.Actual365Fixed(),
        "A/365F": ql.Actual365Fixed(),

        "ACTUAL/365NOLEAP": ql.Actual365NoLeap(),
        "ACT/365NL": ql.Actual365NoLeap(),
        "NL/365": ql.Actual365NoLeap(),
        "ACTUAL/365JGB": ql.Actual365NoLeap(),
        "ACT/365JGB": ql.Actual365NoLeap(),
    }
    _freq_map = {
        "ANNUAL": ql.Annual,
        "SEMIANNUAL": ql.Semiannual,
        "QUARTERLY": ql.Quarterly,
        "BIMONTHLY": ql.Bimonthly,
        "MONTHLY": ql.Monthly,
        "BIWEEKLY": ql.Biweekly,
        "WEEKLY": ql.Weekly,
        "DAILY": ql.Daily
    }
    _day_convention_map = {
        "FOLLOWING": ql.Following,
        "F": ql.Following,
        "MODIFIEDFOLLOWING": ql.ModifiedFollowing,
        "MF": ql.ModifiedFollowing,
        "PRECEDING": ql.Preceding,
        "P": ql.Preceding,
        "MODIFIEDPRECEDING": ql.ModifiedPreceding,
        "MP": ql.ModifiedPreceding,
        "UNADJUSTED": ql.Unadjusted,
        "U": ql.Unadjusted,
        "HALFMONTHMODIFIEDFOLLOWING": ql.HalfMonthModifiedFollowing,
        "HMMF": ql.HalfMonthModifiedFollowing
    }

    # TODO: Find a proper way to catalogue this
    _calendar_map = {
        "US": ql.UnitedStates(),
        "UNITEDSTATES": ql.UnitedStates(),
        "UNITEDSTATES.GOVERNMENTBOND": ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        "GB": ql.UnitedKingdom(),
        "UK": ql.UnitedKingdom(),
        "UNITEDKINGDOM": ql.UnitedKingdom(),
        "JP": ql.Japan(),
        "HK": ql.HongKong(),
        "DE": ql.Germany(),
        "CA": ql.Canada(),
        "AU": ql.Australia()
    }
    _compounding_map = {
        "SIMPLE": ql.Simple,
        "COMPOUNDED": ql.Compounded,
        "CONTINUOUS": ql.Continuous,
        "SIMPLETHENCOMPOUNDED": ql.SimpleThenCompounded
    }
    _date_generation_map = {
        "BACKWARD": ql.DateGeneration.Backward,
        "FORWARD": ql.DateGeneration.Forward,
        "ZERO": ql.DateGeneration.Zero,
        "THIRDWEDNESDAY": ql.DateGeneration.ThirdWednesday,
        "TWENTIETH": ql.DateGeneration.Twentieth,
        "TWENTIETHIMM": ql.DateGeneration.TwentiethIMM,
        "OLDCDS": ql.DateGeneration.OldCDS,
        "CDS": ql.DateGeneration.CDS
    }

    _dg = ql.DateGeneration
    _compounding_set = {ql.Simple, ql.Compounded, ql.Continuous, ql.SimpleThenCompounded}
    _date_generation_set = {_dg.Backward, _dg.Forward, _dg.Zero, _dg.ThirdWednesday,
                            _dg.Twentieth, _dg.TwentiethIMM, _dg.OldCDS, _dg.CDS}


    @classmethod
    def to_daycount(cls, day_count):
        """
        Converts day count str to QuantLib object

        :param day_count: Day count
        :type day_count: str
        :return:
        """
        # remove spaces, parenthesis and capitalize
        if isinstance(day_count, ql.DayCounter):
            return day_count
        else:
            day_count = day_count.upper().translate(None, " ()")
            return cls._daycount_map[day_count]

    @classmethod
    def to_frequency(cls, freq):
        if isinstance(freq, int) or (freq is None):
            return freq
        else:
            try:
                freq = int(freq)
                return freq
            except ValueError as e:
                freq = freq.upper().translate(None, " ")
                return cls._freq_map[freq]
            except:
                raise ValueError("Invalid value for freq")

    @classmethod
    def to_date(cls, date):
        if isinstance(date, ql.Date):
            ql_date = date
        elif isinstance(date, datetime.date ) or isinstance(date, datetime.datetime):
            ql_date = ql.Date(date.day, date.month, date.year)
        elif isinstance(date, str):
            d = parse(date)
            ql_date = ql.Date(d.day, d.month, d.year)
        elif isinstance(date, int):
            year, rest = divmod(date, 10000)
            month, day = divmod(rest, 100)
            ql_date = ql.Date(day, month, year)
        else:
            raise ValueError("Unrecognized date format")
        return ql_date

    @classmethod
    def to_date_yyyymmdd(cls, date):
        if isinstance(date, int):
            yyyymmdd = date
        elif isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            yyyymmdd = date.year*10000 + date.month*100 + date.day
        elif isinstance(date, str):
            d = parse(date)
            yyyymmdd = d.year*10000 + d.month*100 + d.day
        elif isinstance(date, ql.Date):
            yyyymmdd = date.year()*10000 + date.month()*100 + date.dayOfMonth()
        else:
            raise ValueError("Unrecognized date format")
        return yyyymmdd

    @classmethod
    def to_date_py(cls, date):
        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            date_py = date
        elif isinstance(date, str):
            date_py = parse(date).date()
        elif isinstance(date, ql.Date):
            date_py = datetime.date(date.year(), date.month(), date.dayOfMonth())
        elif isinstance(date, int):
            year, rest = divmod(date, 10000)
            month, day = divmod(rest, 100)
            date_py = datetime.date(year, month, day)
        else:
            raise ValueError("Unrecognized date format")
        return date_py

    @classmethod
    def to_template(cls, template):
        from .common import TemplateBase
        if isinstance(template, TemplateBase):
            return template
        elif isinstance(template, str):
            return TemplateBase.lookup_template(template)
        else:
            raise ValueError("Unrecognized instance")

    @classmethod
    def to_day_convention(cls, day_convention):
        day_convention = day_convention.upper().translate(None, " ")
        return cls._day_convention_map[day_convention]

    @classmethod
    def to_calendar(cls, calendar):
        if isinstance(calendar, ql.Calendar):
            return calendar
        else:
            calendar = calendar.upper().translate(None, " ")
            return cls._calendar_map[calendar]

    @classmethod
    def to_compounding(cls, compounding):
        if isinstance(compounding, str):
            compounding = compounding.upper()
            return cls._compounding_map[compounding]
        elif isinstance(compounding, int):
            if compounding in cls._compounding_set:
                return compounding
            else:
                raise ValueError("Invalid compounding value")
        else:
            raise ValueError("Unsupported data type for compounding convention")

    @classmethod
    def to_period(cls, period):
        if isinstance(period, ql.Period):
            return period
        elif isinstance(period, str):
            period = ql.Period(period)
            return period

    @classmethod
    def to_date_generation(cls, rule):
        if isinstance(rule, str):
            rule = rule.upper()
            return cls._date_generation_map[rule]
        elif isinstance(rule, int):
            if rule in cls._date_generation_set:
                return rule
            else:
                raise ValueError("Invalid date generation rule value")