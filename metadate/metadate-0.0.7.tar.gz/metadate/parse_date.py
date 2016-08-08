from datetime import datetime

from dateutil.relativedelta import relativedelta

import metadate.locales.en as locale_en
from metadate.scanner import Scanner

from metadate.classes import MetaRelative
from metadate.classes import MetaDate
from metadate.classes import MetaUnit
from metadate.classes import MetaPeriod
from metadate.classes import Meta


def get_relevant_parts(matches):
    strike = 0
    bundles = [[]]
    for m in matches:
        if m == ' ':
            strike += 1
        else:
            if strike < 3:
                bundles[-1].append(m)
            else:
                bundles.append([m])
            strike = 0
    return bundles


def cleanup_relevant_parts(bundles, locale):
    LEVEL = {u: i for i, u in enumerate(locale.UNITS)}
    cleaned_bundles = []
    for bundle in bundles:
        modifier = False
        meta_units = []
        new = []
        for x in bundle:
            if not isinstance(x, Meta):
                if meta_units:
                    for mu in meta_units:
                        rd = relativedelta(**{mu.unit + 's': mu.amount * locale.MODIFIERS[x.x]})
                        new.append(MetaRelative(rd, level=LEVEL[mu.unit], span=[x.span, mu.span]))
                modifier = x
                meta_units = []
            elif modifier:
                if isinstance(x, MetaUnit):
                    rd = relativedelta(**{x.unit + 's': x.amount * locale.MODIFIERS[modifier.x]})
                    new.append(MetaRelative(rd, level=LEVEL[x.unit], span=[x.span, modifier.span]))
                elif isinstance(x, MetaDate):
                    # if hasattr(x, "month"):
                    #     print("relative", x.month, modifier)
                    # if hasattr(x, "season"):
                    #     print("relative", x.season, modifier)
                    new.append(x)
                elif isinstance(x, MetaRelative):
                    new.append(x)
            elif isinstance(x, MetaUnit):
                meta_units.append(x)
                modifier = False
            else:
                new.append(x)
                meta_unit = []
                modifier = False
        cleaned_bundles.append(new)
    cleaned_bundles = [x for x in cleaned_bundles if any(
        [isinstance(y, MetaDate) or isinstance(y, MetaRelative) for y in x])]
    return cleaned_bundles


def datify(cleaned_bundle, future):
    level = 100
    span = []
    for x in cleaned_bundle:
        s = x.span
        if isinstance(s, list):
            span.extend(s)
        else:
            span.append(s)
    span = sorted(set(span))
    for x in cleaned_bundle:
        if not isinstance(x, Meta):
            continue
        level = min(x.level, level)
    # print(level)
    rds = relativedelta()
    indices = {'year': 0, 'month': 1, 'day': 2, 'hour': 3, 'minute': 4, 'second': 5}
    dts = [-1, -1, -1, -1, -1, -1]
    for d in cleaned_bundle:
        if isinstance(d, MetaDate):
            for x in d.__dict__:
                if x not in ['level', 'span']:
                    dts[indices[x]] = getattr(d, x)
        if isinstance(d, MetaRelative):
            rds += d.rd
    now = datetime.now()
    dt = datetime(year=dts[0] if dts[0] > -1 else now.year,
                  month=dts[1] if dts[1] > -1 else now.month,
                  day=dts[2] if dts[2] > -1 else now.day,
                  hour=dts[3] if dts[3] > -1 else now.hour,
                  minute=dts[4] if dts[4] > -1 else now.minute,
                  second=dts[5] if dts[5] > -1 else now.second)

    start_date = dt + rds
    if level == 7:  # year
        start_date = start_date.replace(month=1, day=1, hour=0, minute=0, second=0)
        end_date = start_date + relativedelta(years=1)
    elif level == 6:  # season
        start_date = start_date.replace(day=21, hour=0, minute=0, second=0)
        end_date = start_date + relativedelta(months=3)
    elif level == 5:  # month
        start_date = start_date.replace(day=1, hour=0, minute=0, second=0)
        end_date = start_date + relativedelta(months=1)
    elif level == 4:  # week
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = start_date + relativedelta(days=7)
    elif level == 3:  # day
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = start_date + relativedelta(days=1)
    elif level == 2:  # hour
        start_date = start_date.replace(minute=0, second=0)
        end_date = start_date + relativedelta(hours=1)
    elif level == 1:  # minute
        start_date = start_date.replace(second=0)
        end_date = start_date + relativedelta(minutes=1)
    elif level == 0:  # second
        end_date = start_date + relativedelta(seconds=1)
    if future and end_date < now:
        start_date = start_date.replace(year=start_date.year + 1)
        end_date = end_date.replace(year=end_date.year + 1)
    elif future and start_date < now:
        start_date = now
    return start_date, end_date, level, span

# flexible for running with a default init of locale_en
en_scanner = Scanner(locale_en)


def parse_date(text, future=True, locale=locale_en, multi=False):
    LEVEL_REV = {i: u for i, u in enumerate(locale.UNITS)}
    scanner = en_scanner if locale == locale_en else Scanner(locale)
    matches, _ = scanner.scan(text)
    parts = get_relevant_parts(matches)
    cleaned_parts = cleanup_relevant_parts(parts, locale)
    if not cleaned_parts:
        return []
    cleaned_parts = sorted(cleaned_parts, key=len, reverse=True)
    if multi:
        multi_results = []
        for cleaned_bundle in cleaned_parts:
            start_date, end_date, level, span = datify(cleaned_bundle, future)
            mp = MetaPeriod(start_date, end_date, LEVEL_REV[level], span, locale.NAME, text)
            multi_results.append(mp)
        return multi_results
    else:
        cleaned_bundle = cleaned_parts[0]
        start_date, end_date, level, span = datify(cleaned_bundle, future)
        mp = MetaPeriod(start_date, end_date, LEVEL_REV[level], span, locale.NAME, text)
        return mp
