import itertools

from dateutil.relativedelta import relativedelta as rd
from datetime import datetime

from metadate.utils import erase_level

t = "every 2 weeks between this year and the next until December on Tuesdays and Wednesdays at ten pm"


class MetaPeriod():

    def __init__(self, start_date, end_date, start_static, end_static, start_interval, end_interval):
        self.start_date = start_date
        self.end_date = end_date
        self.start_static = start_static
        self.end_static = end_static
        self.start_interval = start_interval
        self.end_interval = end_interval

    def cycle(self, now=None):
        bs = self.resolve(self.start_date, 8)
        end = self.resolve(self.end_date, 6)
        es = bs
        print(bs, end)
        for sinterval, einterval in zip(itertools.cycle(self.start_interval),
                                        itertools.cycle(self.end_interval)):
            nbs = bs + sinterval + self.start_static
            nes = bs + einterval + self.end_static
            if nes > end:
                raise StopIteration
            yield nbs, nes
            bs = nbs

    @staticmethod
    def resolve(d, level=8, now=None):
        now = now or datetime.now()
        return erase_level(now, level) + d

    def __repr__(self):
        return "MetaPeriod({}, {}, {})".format(self.start_date, self.end_date, self.interval)

mp = MetaPeriod(rd(years=0),
                rd(years=1, month=12),
                rd(hour=10, minute=0),
                rd(hour=10, minute=1),
                [rd(weeks=2), rd(weekday=4), rd(weekday=5)],
                [rd(weeks=2), rd(weekday=4), rd(weekday=5)])


# for s, e in mp.cycle():
#     print(s, e)
