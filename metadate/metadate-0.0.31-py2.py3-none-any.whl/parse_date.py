import re
import math
from datetime import datetime

from dateutil.relativedelta import relativedelta

import metadate.locales.en as locale_en
from metadate.scanner import Scanner

from metadate.classes import MetaRelative
from metadate.classes import MetaDate
from metadate.classes import MetaOrdinal
from metadate.classes import MetaUnit
from metadate.classes import MetaPeriod
from metadate.classes import MetaModifier
from metadate.classes import MetaRange
from metadate.classes import MetaBetween
from metadate.utils import log
from metadate.utils import UNITS
from metadate.utils import BOUNDARIES
from metadate.utils import erase_level
UNITS_REV = {v: k for k, v in UNITS.items()}


def get_relevant_parts(matches):
    strike = 0
    bundles = [[]]
    for m in matches:
        if isinstance(m, str):
            strike = 1
        else:
            if strike:
                bundles.append([m])
            else:
                bundles[-1].append(m)
            strike = 0
    return bundles


def between_allowed(x, y, text):
    start = x.span[1]
    end = y.span[0]
    return re.match("^[ -]*(and)?[ -]*$", text[start:end])


def merge_ordinal_unit(matches, text):
    news = []
    t = 0
    last = False
    n = len(matches)
    spans = []
    for i, m in enumerate(matches):
        if i != n - 1 and isinstance(m, MetaOrdinal):
            if last and not between_allowed(last, m, text):
                t = 0
            t += float(m.amount)
            last = m
            spans.append(m.span)
            continue
        elif isinstance(m, MetaUnit):
            m.modifier *= t if t else 1
            m.span = [m.span] + spans
            spans = []
        news.append(m)
    return news


def cleanup_relevant_parts(bundles, locale):
    cleaned_bundles = []
    for bundle in bundles:
        modifier = False
        meta_units = []
        new = []
        for x in bundle:
            if isinstance(x, MetaModifier):  # "this"
                if meta_units:
                    for mu in meta_units:
                        rd = relativedelta(**{mu.unit + 's': mu.modifier * locale.MODIFIERS[x.x]})
                        new.append(MetaRelative(rd, level=UNITS[mu.unit], span=[x.span, mu.span]))
                modifier = x
                meta_units = []
            elif modifier:
                if isinstance(x, MetaUnit):
                    if x.unit == "quarter":
                        rd_kwargs = {"months": 3 * x.modifier * locale.MODIFIERS[modifier.x],
                                     "day": 1}
                    else:
                        rd_kwargs = {x.unit + 's': x.modifier * locale.MODIFIERS[modifier.x]}
                    rd = relativedelta(**rd_kwargs)
                    new.append(MetaRelative(rd, level=UNITS[x.unit], span=[x.span, modifier.span]))
                elif isinstance(x, MetaDate):
                    # if hasattr(x, "month"):
                    #     print("relative", x.month, modifier)
                    # if hasattr(x, "season"):
                    #     print("relative", x.season, modifier)
                    new.append(x)
                elif isinstance(x, MetaRelative):

                    if x.rd.weekday is not None:
                        # eg "next" tuesday adds +1 week
                        weeks = locale.MODIFIERS[modifier.x]
                        # "this" also adds +1, "past" should be -1
                        if weeks == 0:
                            weeks = 1
                        x.rd.weeks += weeks
                        modifier = False

                    new.append(x)

            elif isinstance(x, MetaUnit):
                meta_units.append(x)
                modifier = False
            else:
                if not isinstance(x, MetaOrdinal):
                    new.append(x)
                meta_units = []
                modifier = False
        cleaned_bundles.append(new)
    cleaned_bundles = [x for x in cleaned_bundles if any(
        [isinstance(y, MetaDate) or isinstance(y, MetaRelative) for y in x])]
    return cleaned_bundles


def resolve_end_period(start_date, level, future, now):
    future_changed = False
    start_date = erase_level(start_date, level)
    if level == 9:  # year
        end_date = start_date + relativedelta(years=1)
    elif level == 8:  # season
        end_date = start_date + relativedelta(months=3)
    elif level == 7:  # quarter
        for cap in [1, 4, 7, 10]:
            if start_date.month <= cap:
                break
        end_month = (cap + 3)
        if end_month > 12:
            end_date = start_date + relativedelta(month=end_month % 12, day=1, years=1)
        else:
            end_date = start_date + relativedelta(month=end_month, day=1)
    elif level == 6:  # month
        end_date = start_date + relativedelta(months=1)
    elif level == 5:  # week
        end_date = start_date + relativedelta(days=7)
    elif level == 4:  # day
        end_date = start_date + relativedelta(days=1)
    elif level == 3:  # hour
        end_date = start_date + relativedelta(hours=1)
    elif level == 2:  # minute
        end_date = start_date + relativedelta(minutes=1)
    elif level == 1:  # second
        end_date = start_date + relativedelta(seconds=1)
    elif level == 0:  # microsecond
        end_date = start_date + relativedelta(microseconds=1)
    if future and end_date < now:
        start_date = start_date.replace(year=start_date.year + 1)
        end_date = end_date.replace(year=end_date.year + 1)
        future_changed = True
    elif future and start_date < now:
        start_date = now
        future_changed = True
    return start_date, end_date, future_changed


def flatten_inner(l):
    span = []
    for s in l:
        if isinstance(s, list):
            span.extend(flatten_span(s))
        else:
            span.append(s)
    return span


def flatten_span(l):
    return sorted(set(flatten_inner(l)))


def get_min_level(cleaned_bundle):
    level = 100
    for x in cleaned_bundle:
        if isinstance(x, (MetaRelative, MetaUnit, MetaDate)):
            level = min(x.level, level)
    return level


def datify(cleaned_bundle, future):
    now = datetime.now()
    span = flatten_span([x.span for x in cleaned_bundle])
    level = get_min_level(cleaned_bundle)
    # print(level)
    rdt, erdt = resolve_dt(cleaned_bundle, now)
    if erdt is not None:
        start_date = rdt + resolve_rd(cleaned_bundle)
        end_date = erdt + resolve_rd(cleaned_bundle)
        start_date, _, _ = resolve_end_period(start_date, level, future, now)
        end_date = erase_level(erdt, level)
    else:
        resolved_rd = resolve_rd(cleaned_bundle)
        try:
            start_date = rdt + resolved_rd
        except TypeError:
            resolved_rd.years = int(resolved_rd.years)
            resolved_rd.months = int(resolved_rd.months)
            start_date = rdt + resolved_rd

        start_date, end_date, _ = resolve_end_period(start_date, level, future, now)
    return start_date, end_date, level, span

# flexible for running with a default init of locale_en
en_scanner = Scanner(locale_en)


def has_between(bundle):
    return any(isinstance(x, MetaBetween) for x in bundle)


def merge_dt(mdt, dt):
    # mdt is a made-up mutable dt
    # month is precomputed so that day can be init
    month = month = mdt[1] if mdt[1] > -1 else dt.month
    day = mdt[2] if mdt[2] > -1 else dt.day
    ndt = datetime(year=mdt[0] if mdt[0] > -1 else dt.year,
                   month=month,
                   day=min(day, BOUNDARIES[month]),
                   hour=mdt[3] if mdt[3] > -1 else dt.hour,
                   minute=mdt[4] if mdt[4] > -1 else dt.minute,
                   second=mdt[5] if mdt[5] > -1 else dt.second,
                   microsecond=mdt[6] if mdt[6] > -1 else dt.microsecond)
    return ndt


def resolve_dt(cleaned_bundle, now):
    indices = {'year': 0, 'month': 1, 'day': 2, 'hour': 3,
               'minute': 4, 'second': 5, 'microsecond': 6}
    dts = [-1, -1, -1, -1, -1, -1, -1]
    edts = [-1, -1, -1, -1, -1, -1, -1]
    contains_between = has_between(cleaned_bundle)
    for d in cleaned_bundle:
        if isinstance(d, MetaDate):
            for x in d.__dict__:
                if x not in ['level', 'span']:
                    if dts[indices[x]] != -1:
                        if not contains_between:
                            raise ValueError("Field already known in dt, should not overwrite?")
                    else:
                        dts[indices[x]] = getattr(d, x)
                    edts[indices[x]] = getattr(d, x)
    dt = merge_dt(dts, now)
    edt = merge_dt(edts, now) if contains_between else None
    return dt, edt


def resolve_rd(cleaned_bundle):
    indices = {'year': 0, 'month': 1, 'day': 2, 'hour': 3,
               'minute': 4, 'second': 5, 'microsecond': 6}
    rds = relativedelta()
    for d in cleaned_bundle:
        if isinstance(d, MetaRelative):
            rds += d.rd
    return rds


def handle_meta_range(cleaned_bundle, future, locale, text):
    now = datetime.now()
    phase = 0
    mrange = None
    relatives = []
    metadates = []
    for x in cleaned_bundle:
        if phase == 0 and isinstance(x, MetaRange):
            phase = 1
            mrange = x
        elif phase == 1 or phase == 2 and isinstance(x, MetaRelative):
            phase = 2
            relatives.append(x)
        elif phase == 2 or phase == 3 and isinstance(x, MetaDate):
            phase = 3
            metadates.append(x)
    if phase < 2:
        return None
    # case 1: MetaRange, MetaRelative, MetaRelative, etc
    # log("relatives", relatives, True)
    # log("metadates", metadates, True)
    if not metadates:
        # in this case, the start_date becomes "now" adjusted for level
        # the end_date is the start_date + relativedeltas following
        level = get_min_level(relatives)
        rds = relativedelta()
        start_date = erase_level(now, 1)
        for x in relatives:
            rds += x.rd
        try:
            end_date = start_date + rds
        except TypeError:
            rds.years = int(rds.years)
            rds.months = int(rds.months)
            end_date = start_date + rds
        span = flatten_span([mrange.span, [x.span for x in relatives]])
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        return MetaPeriod(start_date, end_date, level, span, locale.NAME, text)
    else:
        spans = flatten_span([flatten_span(x.span) for x in relatives])
        words = [text[x[0]:x[1]].lower() for x in spans]
        # generic
        dt, _ = resolve_dt(metadates, now)
        dt_level = get_min_level(metadates)
        rd_level = get_min_level(relatives)
        if "first" in words:
            # this is actually the logic for !first! days of, not "next days of"
            # case 2: MetaRange, MetaRelative, MetaRelative, etc, MetaDate, Metadate, etc
            start_date, _, future_changed = resolve_end_period(dt, dt_level, future, now)
            end_date = erase_level(dt, dt_level) + resolve_rd(relatives)
        elif "last" in words:
            _, end_date, future_changed = resolve_end_period(dt, dt_level, future, now)
            start_date = erase_level(end_date, dt_level) + resolve_rd(relatives)
        else:
            raise NotImplementedError("What's the case here?")
    if future_changed:
        start_date = start_date + relativedelta(years=1)  # I think also here?
        end_date = end_date + relativedelta(years=1)
    span = flatten_span([mrange.span] + [x.span for x in relatives] +
                        [x.span for x in metadates])
    return MetaPeriod(start_date, end_date, min(rd_level, dt_level), span, locale.NAME, text)


def parse_date(text, future=True, locale=locale_en, multi=False, verbose=False):
    if multi:
        raise NotImplementedError("multi")
    log("\nSentence", text, verbose)
    scanner = en_scanner if locale == locale_en else Scanner(locale)
    matches, _ = scanner.scan(text)
    log("matches", matches, verbose=verbose)
    parts = get_relevant_parts(matches)
    log("1", parts, verbose=verbose)
    merged = [merge_ordinal_unit(x, text) for x in parts]
    log("2", merged, verbose=verbose)
    cleaned_parts = cleanup_relevant_parts(merged, locale)
    log("3", cleaned_parts, verbose)
    if not cleaned_parts:
        return [] if multi else None
    cleaned_parts = sorted(cleaned_parts, key=len, reverse=True)
    now = datetime.now()
    cleaned_bundle = cleaned_parts[0]

    handle_meta_result = handle_meta_range(cleaned_bundle, future, locale, text)
    if handle_meta_result:
        log("4meta", handle_meta_result, verbose)
        return handle_meta_result
    start_date, end_date, level, span = datify(cleaned_bundle, future)
    mp = MetaPeriod(start_date, end_date, UNITS_REV[level], span, locale.NAME, text)
    log("4default", mp, verbose)
    if future and mp.start_date < now:
        return None
    return mp
