from datetime import datetime


def timestamp(dt):
    """
    Utility method for converting datetime.datetime
    to UNIX timestamp.

    """
    if dt.tzinfo:
        utc_dt = dt.replace(tzinfo=None) - dt.utcoffset()
    else:
        utc_dt = dt

    return (utc_dt - datetime(1970, 1, 1)).total_seconds()
