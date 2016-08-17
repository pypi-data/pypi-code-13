# -*- coding: utf-8 -*-
from django import template


def parse_bool_value(value, name):
    """Django templates do not know what a boolean is,
    and anyway we need to support the 'merge' option."""
    if value is None:
        return value
    value = value.lower()
    if value in ('true', '1'):
        return True
    elif value in ('false', '0'):
        return False
    else:
        raise template.TemplateSyntaxError(
            '"%s" argument must be one of the strings '
            '"true" or "false" not "%s"' % (name, value))
