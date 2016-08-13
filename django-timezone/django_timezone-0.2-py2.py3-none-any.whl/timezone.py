import calendar
import datetime as _datetime
import pytz
import six

from django.conf import settings
from django.utils.timezone import (
    get_current_timezone, is_aware, localtime, make_aware, make_naive,
    now as _now)


def date(when=None, tz=None):
    """
    Return a naive ``date`` object for ``when`` in ``tz``. Shortcut for
    ``localize(when, tz).date()``.
    """
    return localize(when, tz).date()


def datetime(
        year, month, day, hour=0, minute=0, second=0, microsecond=0,
        tzinfo=None):
    """
    Return an aware or naive ``datetime`` object. Naive objects will be
    converted to the current timezone.
    """
    when = make_aware(_datetime.datetime(
        year, month, day, hour, minute, second, microsecond), get(tzinfo))
    if not settings.USE_TZ:
        when = make_naive(when, get_current_timezone())
    return when


def get(tz=None):
    """
    Return a ``tzinfo`` object. The default for ``tz`` is the current timezone.
    The ``tz`` argument can be a ``tzinfo`` object or a string. For example,
    "Australia/Sydney".
    """
    if isinstance(tz, six.string_types):
        tz = pytz.timezone(tz)
    return tz or get_current_timezone()


def jstime(when=None):
    """
    Return a ``datetime`` object represented as a JavaScript timestamp
    (milliseconds since 1970).
    """
    # Convert to UTC then return as milliseconds since 1970.
    return calendar.timegm(localize(when, 'UTC').timetuple()) * 1000


def localize(when=None, tz=None):
    """
    Return ``when``, localized (if aware) or converted (if naive) to ``tz``.
    The default for ``when`` is now. The default for ``tz`` is the current
    timezone. The ``tz`` argument can also be given as a string. For example,
    "Australia/Sydney".
    """
    when = when or _now()
    if is_aware(when):
        when = localtime(when, get(tz))
    else:
        when = make_naive(make_aware(when, get_current_timezone()), get(tz))
    return when


def midnight(when=None):
    """
    Return an aware or naive ``datetime`` object for 12:00 AM on ``when``,
    which defaults to now in the current timezone.
    """
    when = when or localize()
    if is_aware(when):
        when = datetime(*when.timetuple()[:3], tzinfo=when.tzinfo)
    else:
        when = _datetime.datetime(*when.timetuple()[:3])
    return when


def now(tz=None):
    """
    Return an aware or naive ``datetime`` object for now in ``tz``. The default
    for ``tz`` is the current timezone. The ``tz`` argument can also be given
    as a string. For example, "Australia/Sydney".
    """
    return localize(tz=None)


def time(when=None, tz=None):
    """
    Return a naive ``time`` object for ``when`` in ``tz``. Shortcut for
    ``localize(when, tz).time()``.
    """
    return localize(when, tz).time()
