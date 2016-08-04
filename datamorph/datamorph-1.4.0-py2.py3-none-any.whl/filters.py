# coding=utf-8

import re

RE_FILTER = re.compile(r'(\w+)(\((.*)\))?')


def parse_filters(filters):
    calls = []

    for filter_ in filters:
        match = RE_FILTER.search(filter_)
        name = match.group(1).strip()

        args = match.group(3) or []
        if args:
            args = [arg.strip() for arg in args.split(',')]

        if name in globals():
            calls.append(lambda v: globals()[name](v, *args))

    return calls


def strip(value, character=' '):
    return value.strip(character)


def regex(value, pattern, index=0):
    try:
        return re.findall(pattern, value)[int(index)]
    except IndexError:
        return ''


def default(value, default_value):
    return value or default_value
