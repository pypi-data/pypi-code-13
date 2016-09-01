"""cubicweb-oaipmh application package

OAI-PMH server for CubicWeb
"""
from datetime import datetime
from collections import namedtuple

from isodate import datetime_isoformat
import pytz

from logilab.common.deprecation import deprecated


@deprecated('[oaipmh 0.2] use isodate.datetime_isoformat')
def isodate(date=None):
    if date is None:
        date = utcnow()
    return datetime_isoformat(date)


def utcnow():
    return datetime.now(tz=pytz.utc)


# Model for metadata format of records in the OAI-PMH repository.
MetadataFormat = namedtuple('MetadataFormat', ['schema', 'namespace'])
