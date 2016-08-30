import re

UNITS = {
    'microsecond': 0,
    'second': 1,
    'minute': 2,
    'hour': 3,
    'day': 4,
    'week': 5,
    'month': 6,
    'quarter': 7,
    'season': 8,
    'year': 9
}


def log(tag, x, verbose=False):
    if verbose:
        print("--- {} ------------".format(tag))
        print(x)


def add_tag(sentence, matches, color="mediumspringgreen"):
    # given textual matches between ranges like [(5, 10), (10, 15)]
    # this will clean up
    # first is 0,5
    news = ''
    lbound = 0
    hit = "<span style='background-color:{}'>{}</span>"
    for m in matches:
        news += sentence[lbound:m[0]]
        news += hit.format(color, sentence[m[0]:m[1]])
        lbound = m[1]
    news += sentence[matches[-1][1]:]
    return news


def strip_pm(txt, numbers_dict=None):
    txt = txt.lower()
    hoffset = 12 * ('pm' in txt or "afternoon" in txt or 'p.m' in txt)
    txt = txt.replace("afternoon", "")
    if numbers_dict is None:
        parts = re.sub("[:hapm.]+", " ", txt).split()
    else:
        parts = re.sub(" ?[ap][.]?m[.]?$", " ", txt).split()
    parts = [x for x in parts if x]
    microsecond = None
    second = None
    minute = None
    if len(parts) == 4:
        hour, minute, second, microsecond = parts
    elif len(parts) == 3:
        hour, minute, second = parts
    elif len(parts) == 2:
        hour, minute = parts
    else:
        hour = parts[0]
    if numbers_dict is not None:
        hour = numbers_dict[hour]
    if int(hour) == 12 and hoffset:
        hoffset = 0
    hour = (hoffset + int(hour)) % 24
    return hour, minute, second, microsecond


def erase_level(d, level):
    if level == 9:    # year
        d = d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif level == 8:  # season
        d = d.replace(day=21, hour=0, minute=0, second=0, microsecond=0)
    elif level == 7:  # quarter
        d = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif level == 6:  # month
        d = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif level == 5:  # week
        d = d.replace(hour=0, minute=0, second=0, microsecond=0)
    elif level == 4:  # day
        d = d.replace(hour=0, minute=0, second=0, microsecond=0)
    elif level == 3:  # hour
        d = d.replace(minute=0, second=0, microsecond=0)
    elif level == 2:  # minute
        d = d.replace(second=0, microsecond=0)
    elif level == 1:  # second
        d = d.replace(microsecond=0)
    return d


BOUNDARIES = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}
