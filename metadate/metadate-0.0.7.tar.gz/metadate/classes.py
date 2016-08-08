from datetime import datetime
from collections import namedtuple

labels = ["start_date", "end_date", "level", "spans", "locale"]
MetaPeriod = namedtuple("MetaPeriod", labels)

units = ['second', 'minute', 'hour', 'day', 'week', 'month', 'season', 'year']


class Meta(object):
    pass


class MetaPeriod(Meta):

    def __init__(self, start_date, end_date, level, spans, locale, text):
        self.start_date = start_date
        self.end_date = end_date
        self.level = level
        self.spans = spans
        self.locale = locale
        self.text = text
        self.matches = [text[i:j] for i, j in spans]

    def __repr__(self):
        name = self.__class__.__name__
        cases = ['start_date', 'end_date', 'level', 'matches', 'locale']
        n = len(name) + 1
        atts = {x: str(getattr(self, x)) for x in cases if getattr(self, x, None) is not None}
        sep = ',\n' + ' ' * n
        values = sep.join(["{}={}".format(x, atts[x]) for x in cases if x in atts])
        return "{}({})".format(name, values)


class MetaDate(Meta):

    def __init__(self, span, **kwargs):
        self.span = span
        self.__dict__.update({k: int(v) for k, v in kwargs.items()})
        self.level = min([units.index(x) for x in self.__dict__ if x != 'span'])

    def __repr__(self):
        cases = ['second', 'minute', 'hour', 'day', 'week', 'month', 'season', 'year']
        cases += ['level', 'span']
        atts = {x: str(getattr(self, x)) for x in cases if getattr(self, x, None) is not None}
        values = ', '.join(["{}={}".format(x, atts[x]) for x in cases if x in atts])
        return "{}({})".format(self.__class__.__name__, values)

    def to_dt(self):
        now = datetime.now()
        year = getattr(self, "year", now.year)
        month = getattr(self, "month", now.month)
        day = getattr(self, "day", now.day)
        hour = getattr(self, "hour", now.hour)
        minute = getattr(self, "minute", now.minute)
        second = getattr(self, "second", now.second)
        return datetime(year, month, day, hour, minute, second)


class MetaUnit(Meta):

    def __init__(self, amount, unit, span, modifier=None):
        self.amount = int(amount)
        self.unit = unit
        self.span = span
        self.level = units.index(unit)
        self.modifier = modifier

    def __repr__(self):
        cases = ["amount", "unit", "modifier", "span"]
        atts = {x: str(getattr(self, x)) for x in cases if getattr(self, x, None) is not None}
        values = ', '.join(["{}={}".format(x, atts[x]) for x in cases if x in atts])
        return "{}({})".format(self.__class__.__name__, values)


class MetaRelative(Meta):

    def __init__(self, rd, level, span):
        self.span = span
        self.rd = rd
        self.level = level

    def __repr__(self):
        msg = "{}(rd={}, level={}, span={})"
        return msg.format(self.__class__.__name__, self.rd, self.level, self.span)
