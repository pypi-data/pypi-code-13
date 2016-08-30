import itertools
from datetime import datetime

from dateutil.relativedelta import relativedelta as rd

from metadate.utils import erase_level
from dateutil.rrule import rrule

list(rrule(5, count=2, byweekday=1))


class MetaPeriod():

    def __init__(self, start_date, end_date, start_static, end_static, interval):
        self.start_date = start_date
        self.end_date = end_date
        self.start_static = start_static
        self.end_static = end_static
        self.interval = interval

    def cycle(self, now=None):
        now = now or datetime.now()
        bs = self.resolve(self.start_date, 9, now)
        end = self.resolve(self.end_date, 9, now)
        yield bs + self.start_static, bs + self.end_static
        for interval in itertools.cycle(self.interval):
            nbs = bs + self.start_static + interval
            nes = bs + self.end_static + interval
            if nes == end:
                yield nbs, nes
                raise StopIteration
            if nes > end:
                raise StopIteration
            yield nbs, nes
            bs = nbs

    @staticmethod
    def resolve(d, level=9, now=None):
        now = now or datetime.now()
        return erase_level(now, level) + d

    def __repr__(self):
        return "MetaPeriod({}, {}, {})".format(self.start_date, self.end_date, self.interval)

# and and or make both go into the interval list
t = "every 2 weeks between this year and the next until December on Tuesdays and Wednesdays at ten pm"
mp = MetaPeriod(rd(hour=10, years=0),
                rd(hour=10, years=1, month=12),
                rd(minute=0),
                rd(minute=1),
                [rd(weekday=4), rd(weekday=5), rd(weeks=2)])

"Every 3 hours from 9 AM to 5 PM"

mp = MetaPeriod(rd(day=5, month=10, year=2017, hour=9),
                rd(day=5, month=10, year=2017, hour=17),
                rd(hours=0),
                rd(hours=1),
                [rd(hours=3)])

for s, e in mp.cycle():
    print(s, e)
