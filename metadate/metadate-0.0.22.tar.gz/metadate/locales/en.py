NAME = "en"

# make it not based on index, but key val, and include "hrs", "wks"
UNITS = {
    'microsecond': 'microsecond',
    'second': 'second',
    'minute': 'minute',
    'hour': 'hour',
    'day': 'day',
    'week': 'week',
    'month': 'month',
    'season': 'season',
    'year': 'year'
}


MODIFIERS = {
    "in": 1,
    "on": 0,
    "this": 0,
    "for": 0,
    "next":  1,
    "coming": 1,
    "after": 1,
    "before": -1,
    'recent': -1,
    'past': -1,
    # untested from here
    "previous": -1,
    "last": -1,
    "first": 1,
    "ago": -1,
    "earlier": -1
}

ORDINAL_NUMBERS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'few': 3,
    'a couple': 3,
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
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
}

IN_THE = ['in the', 'over the', 'during the', 'within the', 'for']

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7,
    "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}
MONTHS_SHORTS = {k[:3]: v for k, v in MONTHS.items()}

WEEKDAY = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

WEEKDAY_SHORTS = {k[:3]: v for k, v in WEEKDAY.items()}

SEASONS = {
    "winter": 12,
    "spring": 3,
    "summer": 6,
    "fall": 9,
    "autumn": 9
}

TODAY_TOMORROW = {
    "today": 0,
    "tomorrow": 1,
    "yesterday": -1
}

NOON = {
    "noon": 12,
    "midnight": 0
}

AND = ["and"]

RANK_NAMING = ['st', 'nd', 'rd', 'th']
ON_THE = ['on the']

WHITELIST = ["at", "of", ",", "the"]
