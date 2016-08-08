# XXX: something with the name of the days
# DAYNAMES = []
NAME = "en"

UNITS = ['second', 'minute', 'hour', 'day', 'week', 'month', 'season', 'year']

MODIFIERS = {
    "in": 1,
    "on": 0,
    "the": 0,
    "this": 0,
    "next":  1,
    "coming": 1,
    "after": 1,
    "before": -1,
    # untested from here
    "previous": -1,
    "last": -1,
    "ago": -1
}

ORDINAL_NUMBERS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'fourty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety,': 90,
    'hundred,': 100,
    'thousand': 1000,
}

MONTHS = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7,
          "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

MONTHS_SHORTS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
                 "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

SEASONS = {
    "winter": 12,
    "spring": 3,
    "summer": 6,
    "fall": 9,
    "autumn": 9
}

TODAY_TOMORROW = {
    "today": 0,
    "tomorrow": 1
}

AND = ["and"]

RANK_NAMING = ['st', 'nd', 'th']
ON_THE = ['on the']

LEVEL = {u: i for i, u in enumerate(UNITS)}
