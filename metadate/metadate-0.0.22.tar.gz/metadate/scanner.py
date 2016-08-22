import re
from itertools import product
from dateutil.relativedelta import relativedelta
from metadate.classes import MetaRelative
from metadate.classes import MetaDate
from metadate.classes import MetaOrdinal
from metadate.classes import MetaUnit
from metadate.classes import MetaRange
from metadate.classes import MetaModifier
from metadate.utils import strip_pm
from metadate.utils import UNITS

YEAR = ["[12][0-9]{3}"]
MONTH = ["0?[1-9]", "1[0-2]"]
DAY = ['[12][0-9]', '[3][01]', '0[1-9]', '[0-9]']
SEP = ['[ -/]']
HOUR = ['[01][0-9]', '2[0-3]', '[0-9]']
MINUTE = ['[0-5][0-9]']
SECOND = ['[0-5][0-9]']
END = [r'\b']
APM = [" ?am", " ?pm"]


def pipe(ls, pre=r'\b', post=r''):
    # this is flipped
    p = post + "|" + pre
    return pre + p.join(ls) + post


class Scanner():

    def __init__(self, locale, re_flags=re.IGNORECASE):
        self.__dict__.update({k: v for k, v in locale.__dict__.items() if not k.startswith("__")})

        self.blacklist = []
        for k, v in locale.__dict__.items():
            if isinstance(v, (dict, list)) and k == k.upper():
                self.blacklist.extend(list(v))

        self.HH_MM_SS = self.scan_product(END, HOUR, [":", "h"], MINUTE, [":", "m"],
                                          SECOND, APM + ["m", ''], END)
        self.HH_MM_SS_m = self.scan_product(END, HOUR, [":", "h"], MINUTE, [":", "m"],
                                            SECOND, ['\.\d+'], END)

        self.HH_MM = self.scan_product(END, HOUR, [":", "h"], MINUTE, APM + ["m", ""], END)
        self.HH_MM2 = self.scan_product(END, HOUR, ["."], MINUTE, APM, END)
        self.HHAPM = self.scan_product(END, HOUR, APM, END)
        self.YYYY_MM_DD = self.scan_product(END, YEAR, SEP, MONTH, SEP, DAY)
        self.YYYYMMDD = self.scan_product(END, YEAR, MONTH, DAY)
        self.DD_MM_YYYY = self.scan_product(END, DAY, SEP, MONTH, SEP, YEAR)
        self.DDMMYYYY = self.scan_product(END, DAY, MONTH, YEAR)
        self.YYYY = self.scan_product(END, YEAR)
        self.DDMM = self.scan_product(END, ["\d{1,2}"], ["..", ""], [" of ", " "], self.MONTHS)
        self.DDMMS = self.scan_product(END, ["\d{1,2}"], ["..", ""], [
                                       " of ", " "], self.MONTHS_SHORTS)
        self.ORDINAL = self.scan_product(END, self.ORDINAL_NUMBERS, [" "])
        self.ON_THE_DAY = self.scan_product(END, self.ON_THE, DAY, self.RANK_NAMING, END)

        # IN_THE = ['in the', 'over the', 'during the']
        # LAST_FIRST = {
        #     'last': -1,
        #     'first': 1
        # }

        # MODIFIERS = {
        #     "in": 1,
        #     "on": 0,
        #     "this": 0,
        #     "next":  1,
        #     "coming": 1
        # }

        self.scanner = re.Scanner([
            (self.HH_MM_SS_m, self.hh_mm_ss),
            (self.HH_MM_SS, self.hh_mm_ss),
            (self.HH_MM, self.hh_mm),
            (self.HH_MM2, self.hh_mm),
            (self.HHAPM, self.hh_mm),
            (self.YYYY_MM_DD, self.yyyy_mm_dd),
            (self.YYYYMMDD, self.yyyymmdd),
            (self.DD_MM_YYYY, self.dd_mm_yyyy),
            (self.DDMMYYYY, self.ddmmyyyy),
            (self.YYYY, self.yyyy),                      # YYYY
            (self.ORDINAL, self.ordinal),
            (pipe(self.IN_THE, post=" "), self.in_the),
            (pipe(self.TODAY_TOMORROW), self.today_tomorrow),
            (pipe(self.MODIFIERS), lambda y, x: MetaModifier(x.lower(), y.match.span())),
            (pipe(self.SEASONS), self.season),
            (pipe(self.MONTHS, post=r" [0-3]?[0-9]\b"), self.letter_month_day),
            (pipe(self.MONTHS_SHORTS, post=r" [0-3]?[0-9]\b"), self.short_day_month),
            (self.DDMM, self.ddmm),
            (self.DDMMS, self.ddmms),
            (pipe(self.MONTHS), self.letter_month),
            (pipe(self.MONTHS_SHORTS), self.short_month),
            (pipe(self.WEEKDAY, post=r's?\b'), self.weekday),
            (pipe(self.WEEKDAY_SHORTS, post=r's?\b'), self.weekday_shorts),
            (self.ON_THE_DAY, self.on_the_day),
            ("and a half", lambda y, x: MetaOrdinal("0.5", span=y.match.span())),
            # (self.ON_THE_DAY, self.on_the_day_ordinal),
            (pipe(self.UNITS, r'\b', 's?'), lambda y, x: MetaUnit(
                self.UNITS[x.rstrip("s")], span=y.match.span())),
            (r"\d+", lambda y, x: MetaOrdinal(x, span=y.match.span())),
            # tricky stuff
            (pipe(self.AND), None),  # anding means just like ignoring
            (pipe(self.blacklist), None),
            (r' +', None),
            (r'.', lambda y, x: x)
        ], re_flags)

    def scan(self, text):
        return self.scanner.scan(text)

    @staticmethod
    def scan_product(*args):
        return '|'.join([''.join(x) for x in product(*args)])

    def season(self, y, x):
        return MetaRelative(relativedelta(month=self.SEASONS[x.lower()], day=21), level=7, span=y.match.span())

    def in_the(self, y, x):
        s, e = y.match.span()
        e -= 1
        r = MetaRange(x.rstrip(" "), span=(s, e))
        return r

    def letter_month_day(self, y, x):
        # June 16
        month, day = x.lower().split()
        return MetaDate(month=self.MONTHS[month], day=day, span=y.match.span())

    def letter_day_month(self, y, x):
        # 16 June
        day, month = x.lower().split()
        return MetaDate(month=self.MONTHS[month], day=day, span=y.match.span())

    def short_month_day(self, y, x):
        month, day = x.lower().split()
        return MetaDate(month=self.MONTHS_SHORTS[month], day=day, span=y.match.span())

    def short_day_month(self, y, x):
        day, month = x.lower().split()
        return MetaDate(month=self.MONTHS_SHORTS[month], day=day, span=y.match.span())

    def weekday(self, y, x):
        # Tuesday
        weekday = self.WEEKDAY[x.lower().rstrip("s")]
        return MetaRelative(relativedelta(weekday=weekday), level=4, span=y.match.span())

    def weekday_shorts(self, y, x):
        # Tuesday
        weekday = self.WEEKDAY_SHORTS[x.lower().rstrip("s")]
        return MetaRelative(relativedelta(weekday=weekday), level=4, span=y.match.span())

    def ddmm(self, y, x):
        parts = x.split()
        day, month = re.sub("[^0-9]", "", parts[0]), parts[-1].lower()
        return MetaDate(month=self.MONTHS[month], day=day, span=y.match.span())

    def ddmms(self, y, x):
        parts = x.split()
        day, month = re.sub("[^0-9]", "", parts[0]), parts[-1].lower()
        return MetaDate(month=self.MONTHS_SHORTS[month], day=day, span=y.match.span())

    def letter_month(self, y, x):
        return MetaDate(month=self.MONTHS[x.lower()], span=y.match.span())

    def short_month(self, y, x):
        return MetaDate(month=self.MONTHS_SHORTS[x.lower()], span=y.match.span())

    def today_tomorrow(self, y, x):
        days = self.TODAY_TOMORROW[x.lower()]
        return MetaRelative(relativedelta(days=days), level=4, span=y.match.span())

    def th_of_month(self, y, x):
        # 25th of June
        parts = x.lower().split()
        dayth, month = parts[0][:-2], parts[-1]
        return MetaDate(month=self.MONTHS[month], day=dayth, span=y.match.span())

    @staticmethod
    def hh_mm_ss(y, x):
        hour, minute, second, microsecond = strip_pm(x)
        if "." in x:
            md = MetaDate(hour=hour, minute=minute, second=second,
                          microsecond=microsecond, span=y.match.span())
        else:
            md = MetaDate(hour=hour, minute=minute, second=second, span=y.match.span())
        return md

    @staticmethod
    def hh_mm(y, x):
        hour, minute, _, _ = strip_pm(x)
        if minute is None:
            return MetaDate(hour=hour, span=y.match.span())
        return MetaDate(hour=hour, minute=minute, span=y.match.span())

    def ordinal(self, y, x):
        return MetaOrdinal(self.ORDINAL_NUMBERS[x.lower().strip()], span=y.match.span())

    @staticmethod
    def yyyy_mm_dd(y, x):
        year, month, day = re.split("[ /-]", x)
        return MetaDate(year=year, month=month, day=day, span=y.match.span())

    @staticmethod
    def yyyymmdd(y, x):
        return MetaDate(year=x[:4], month=x[4:6], day=x[6:8], span=y.match.span())

    @staticmethod
    def dd_mm_yyyy(y, x):
        day, month, year = re.split("[ /-]", x)
        return MetaDate(year=year, month=month, day=day, span=y.match.span())

    @staticmethod
    def ddmmyyyy(y, x):
        return MetaDate(year=x[4:8], month=x[2:4], day=x[:2], span=y.match.span())

    @staticmethod
    def dd(y, x):
        return MetaDate(day=x, span=y.match.span())

    @staticmethod
    def yyyy(y, x):
        return MetaDate(year=x, span=y.match.span())

    @staticmethod
    def on_the_day(y, x):
        # "on the 31st"
        return MetaDate(day=x.split()[2][:-2], span=y.match.span())
