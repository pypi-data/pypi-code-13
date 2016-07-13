"""
Provides various utility functions and decorators.
"""
from functools import wraps

from jsonschema import (validate as jsonschema_validate,
                        ValidationError as JsonSchemaValidationError,
                        FormatChecker)

from untt.ex import ValidationError


def normalize_docsplit(docsplit):
    """
    Strips the lines and the line list.
    """
    docsplit = [l.strip() for l in docsplit]

    if len(docsplit) > 0:
        if docsplit[0] == '':
            docsplit = docsplit[1:]

    if len(docsplit) > 0:
        if docsplit[-1] == '':
            docsplit = docsplit[:-1]

    return docsplit


def parse_docstring(doc):
    """
    Parses title and description out of a docstring.
    """
    doc_split = normalize_docsplit(doc.split('\n'))
    if len(doc_split) == 0:
        return '', ''
    elif len(doc_split) == 1:
        return doc_split[0], ''

    if doc_split[1] != '':
        return '', '\n'.join(doc_split)
    else:
        title = doc_split[0]
        description = '\n'.join(doc_split[2:])

        return title, description


def entity_base(klass):
    """
    Indicates that an `Entity` is a base and not an actual one.

    Entities decorated with this decorator will not be included in the root
    schema definitions.
    """
    del klass.schema_definitions[klass.__name__]
    return klass


@wraps(jsonschema_validate)
def validate(*args, **kwargs):
    """
    jsonschema.validate wrapper, that raises `untt.ex.ValidationError`.
    """
    try:
        jsonschema_validate(*args, **kwargs, format_checker=FormatChecker())
    except JsonSchemaValidationError as ex:
        raise ValidationError(str(ex)) from ex


class EmptyValue(object):
    """Used to represent an empty dummy value."""
    pass
