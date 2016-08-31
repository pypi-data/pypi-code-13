

from datetime import datetime, timedelta, tzinfo

import time
import random
import hashlib
import os
import re

RE_NUMERIC_INT = re.compile(r'^\d+$')
RE_NUMERIC_FLOAT = re.compile(r'^\d(\.\d+)?(E\d+)?$')



def md5(*text):
    checksum = hashlib.md5(text[0])
    for i in text[1:]:
        checksum.update(i)
    return checksum.hexdigest()


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return timedelta(0)


class datetime8601(datetime):

    ISO_8601_FORMAT = "%Y-%m-%d %H:%M:%S.%fZ"
    COOKIE_TIME = "%a, %d %b %Y %H:%M:%S GMT"

    @classmethod
    def to8601(cls, instance):
        _format = cls.ISO_8601_FORMAT
        return instance.strftime(_format)

    @classmethod
    def from8601(cls, timestring_8601):
        _format = cls.ISO_8601_FORMAT
        return cls.strptime(timestring_8601, _format)

    @property
    def iso8601(self):
        return self.to8601(self)

    def __str__(self):
        return self.to8601(self)

    @classmethod
    def tzaware(cls, dt, tz=None):
        return datetime(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second,
            tzinfo=tz)


def is_prod_server():
    service = os.environ.get('SERVER_SOFTWARE', None)
    if isinstance(service, basestring):
        return (service.startswith('Google App Engine') or
                service.startswith('AppScaleServer'))
    # else
    return False

def is_dev_server():
    params = (
        ('Development', 'SERVER_SOFTWARE'),
        ('dev', 'APPLICATION_ID')
    )
    for prefix, attrib in params:
        value = os.environ.get(attrib, None)
        if value is not None and value.startswith(prefix):
            return True
    # else
    return False

# Parses expressions like "a[0].prop"
RE_DOTSEP_SPLITTER = re.compile(r'\.|\[(\d+)\]')


def dotsep_split(expr):
    return filter(bool, RE_DOTSEP_SPLITTER.split(expr))


def dict_resolve(base, expr, default=None):
    """Resolve a dot-notation path within nested dictionaries."""
    data = base
    for k in dotsep_split(expr):
        if (data is None) or (not isinstance(data, (dict, list))):
            return default
        if isinstance(data, list) and RE_NUMERIC_INT.match(k):
            data = data[int(k)]
        elif isinstance(data, dict):
            data = data.get(k, default)
    return data


def dict_extend(target, *sources):
    for source in sources:
        for k, v in source.iteritems():
            if k not in target:
                target[k] = v
    return target



class odict(dict):
    """
    Simple object notation wrapper on Dictionary.

    Allows to declare an object by (nested) dictionary and access its elements
    as object properties.

    Example:
        temp = odict(value={'two': 7})
        assert (temp.value.two == 7)
    """

    def __init__(self, *items, **attribs):
        stage = {}
        for k, v in attribs.items():
            if isinstance(v, dict):
                v = odict(**v)
            if isinstance(v, list):
                v = [(odict(i) if isinstance(i, dict) else i) for i in v]
            stage[k] = v
        super(odict, self).__init__(*items, **stage)

    def __getattr__(self, name, default=None):
        return self.get(name, default)

    def __setattr__(self, name, value):
        self[name] = value



def relative_seconds(seconds):
    return datetime.utcnow() + timedelta(seconds=int(seconds))


def expires_time(t):
    if isinstance(t, (int, float, long)):
        t = relative_seconds(t)
    if isinstance(t, datetime):
        t = datetime8601.tzaware(t, UTC())
        return t.strftime("%a, %d %b %Y %H:%M:%S %Z")
    else:
        raise TypeError("expires_time requires a datetime instance")


def expires_time_parse(s):
    t = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z")
    return datetime8601.tzaware(t, UTC())


BASE62_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62encode(value, charset=BASE62_CHARS):
    result, base = [], len(charset)
    while value:
        value, radix = divmod(value, base)
        result.append(charset[radix])
    result.reverse()
    return ''.join(result)


def base62decode(value_str, charset=BASE62_CHARS):
    result, base = 0L, len(charset)
    for c in value_str:
        result *= base
        result += charset.index(c)
    return result


# This is NOT guaranteed to produce UNIQUE values
# In my test it generates approximately 0.035% duplicates
# in a batch of 1,000,000 over approximately 5 seconds.
# This is deemed acceptable with logic to re-try when true
# unique values are required.
def timecode_random_offset(ts):
    intpart, radpart = divmod(ts, 1)
    intpart = int(intpart)
    radpart = int(radpart * 10E6) + 1
    randpart = (random.randint(1, intpart))
    return randpart ^ ((intpart + radpart) % radpart)


def generate_unique_timecode():
    hashnum = timecode_random_offset(time.time())
    return base62encode(hashnum)


def extract_domain(user_email):
    return user_email[user_email.find('@') + 1:]


def user_in_domain(user_email, domain):
    test_within = domain.split('.')
    user_domain = extract_domain(user_email).split('.')
    return user_domain[-(len(test_within)):] == test_within
