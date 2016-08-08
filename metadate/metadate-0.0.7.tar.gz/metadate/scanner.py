import re
from itertools import product
from dateutil.relativedelta import relativedelta
from metadate.classes import MetaRelative
from metadate.classes import MetaDate
from metadate.classes import MetaUnit
from collections import namedtuple

YEAR = ["[12][0-9]{3}"]
MONTH = ["0[1-9]", "1[0-2]"]
DAY = ['[12][0-9]', '[3][01]', '[0-9]', '0[0-9]']  # pipe(, post=r'[^0-9]')
SEP = ['[ -/]']
HOUR = ['[01][0-9]', '2[0-3]']
MINUTE = ['[0-5][0-9]']
SECOND = ['[0-5][0-9]']
END = [r'\b']


def pipe(ls, pre=r'\b', post=r''):
    # this is flipped
    p = post + "|" + pre
    return pre + p.join(ls) + post


Match = namedtuple("Match", ["x", "span", "name"])


class Scanner():

    def __init__(self, locale):
        self.__dict__.update({k: v for k, v in locale.__dict__.items() if not k.startswith("__")})

        self.HH_MM_SS = self.scan_product(END, HOUR, [":"], MINUTE, [":"], SECOND)
        self.HH_MM = self.scan_product(END, HOUR, [":"], MINUTE)
        self.YYYY_MM_DD = self.scan_product(END, YEAR, SEP, MONTH, SEP, DAY)
        self.YYYYMMDD = self.scan_product(END, YEAR, MONTH, DAY)
        self.DD_MM_YYYY = self.scan_product(END, DAY, SEP, MONTH, SEP, YEAR)
        self.DDMMYYYY = self.scan_product(END, DAY, MONTH, YEAR)
        self.YYYY = self.scan_product(END, YEAR)
        self.ORDINAL_UNIT = self.scan_product(END, self.ORDINAL_NUMBERS, [" "], self.UNITS)
        self.ON_THE_DAY = self.scan_product(END, self.ON_THE, DAY, self.RANK_NAMING, END)

        self.scanner = re.Scanner([
            (self.HH_MM_SS, self.hh_mm_ss),
            (self.HH_MM, self.hh_mm),
            (self.YYYY_MM_DD, self.yyyy_mm_dd),
            (self.YYYYMMDD, self.yyyymmdd),
            (self.DD_MM_YYYY, self.dd_mm_yyyy),
            (self.DDMMYYYY, self.ddmmyyyy),
            (self.YYYY, self.yyyy),                      # YYYY
            (self.ORDINAL_UNIT, self.ordinal_unit),
            (pipe(self.TODAY_TOMORROW), self.today_tomorrow),
            (pipe(self.MODIFIERS), lambda y, x: Match(x.lower(), y.match.span(), name="modifier")),
            (pipe(self.SEASONS), self.season),
            (pipe(self.MONTHS, post=r" [0-3]?[0-9]\b"), self.letter_month_day),
            (pipe(self.MONTHS, pre=r"\b[0-3]?[0-9].. of "), self.th_of_month),
            (pipe(self.MONTHS), self.letter_month),
            (pipe(self.MONTHS_SHORTS), self.short_month),
            (self.ON_THE_DAY, self.on_the_day),
            (pipe(self.UNITS, r'\b\d+ '), lambda y, x: MetaUnit(*x.split(), span=y.match.span())),
            (pipe(self.UNITS, r'\b', 's?'), lambda y, x: MetaUnit(1, x, span=y.match.span())),
            # tricky stuff
            (pipe(self.AND), None),  # anding means just like ignoring
            (r' +', " "),
            (r'.', None)
        ], re.IGNORECASE)

    def scan(self, text):
        return self.scanner.scan(text)

    @staticmethod
    def scan_product(*args):
        return '|'.join([''.join(x) for x in product(*args)])

    def season(self, y, x):
        return MetaRelative(relativedelta(month=self.SEASONS[x], day=21), level=6, span=y.match.span())

    def letter_month_day(self, y, x):
        # June 16
        month, day = x.lower().split()
        return MetaDate(month=self.MONTHS[month], day=day, span=y.match.span())

    def short_month_day(self, y, x):
        month, day = x.lower().split()
        return MetaDate(month=self.MONTHS_SHORTS[month], day=day, span=y.match.span())

    def letter_month(self, y, x):
        return MetaDate(month=self.MONTHS[x.lower()], span=y.match.span())

    def short_month(self, y, x):
        return MetaDate(month=self.MONTHS_SHORTS[x.lower()], span=y.match.span())

    def today_tomorrow(self, y, x):
        days = self.TODAY_TOMORROW[x.lower()]
        return MetaRelative(relativedelta(days=days), level=3, span=y.match.span())

    def th_of_month(self, y, x):
        # 25th of June
        parts = x.lower().split()
        dayth, month = parts[0][:-2], parts[-1]
        return MetaDate(month=self.MONTHS[month], day=dayth, span=y.match.span())

    @staticmethod
    def hh_mm_ss(y, x):
        return MetaDate(hour=x[:2], minute=x[3:5], second=x[6:8], span=y.match.span())

    def ordinal_unit(self, y, x):
        amount, unit = x.split()
        return MetaUnit(self.ORDINAL_NUMBERS[amount.lower()], unit, span=y.match.span())

    @staticmethod
    def hh_mm(y, x):
        return MetaDate(hour=x[:2], minute=x[3:5], span=y.match.span())

    @staticmethod
    def yyyy_mm_dd(y, x):
        return MetaDate(year=x[:4], month=x[5:7], day=x[8:10], span=y.match.span())

    @staticmethod
    def yyyymmdd(y, x):
        return MetaDate(year=x[:4], month=x[4:6], day=x[6:8], span=y.match.span())

    @staticmethod
    def dd_mm_yyyy(y, x):
        return MetaDate(year=x[6:10], month=x[3:5], day=x[:2], span=y.match.span())

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
