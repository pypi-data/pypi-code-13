import re

UNITS = {
    'microsecond': 0,
    'second': 1,
    'minute': 2,
    'hour': 3,
    'day': 4,
    'week': 5,
    'month': 6,
    'season': 7,
    'year': 8
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


def strip_pm(txt):
    hoffset = 12 * ('pm' in txt.lower())
    parts = re.sub("[:hapm.]", " ", txt).split()
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
    if int(hour) == 12 and hoffset:
        hoffset = 0
    hour = (hoffset + int(hour)) % 24
    return hour, minute, second, microsecond

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
