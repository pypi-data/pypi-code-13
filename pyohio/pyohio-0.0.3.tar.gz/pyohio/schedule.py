import requests
import requests_cache
from collections import OrderedDict
from datetime import datetime
from dateutil import parser
from operator import itemgetter
from tabulate import tabulate

SCHEDULE_URL = "http://pyohio.org/schedule/json/"

def get_schedule(cache_ttl=3600):
    """ Get the schedule from the conference website and return the JSON. """
    requests_cache.install_cache(expire_after=cache_ttl)
    response = requests.get(SCHEDULE_URL)
    response.raise_for_status()
    return response.json()

def _session_summary(session):
    """ Given a detailed session dict, return a summary dict. """
    summary = OrderedDict()
    summary['date'] = parser.parse(session.get('start', '2016')).date().isoformat()
    summary['start_time'] = parser.parse(session.get('start', '2016')).time().strftime('%H:%M')
    summary['end_time'] = parser.parse(session.get('end', '2016')).time().strftime('%H:%M')
    summary['room'] = session.get('room')
    summary['name'] = session.get('name')
    authors = session.get('authors', []) or []
    summary['presenter'] = ", ".join(authors)
    return summary

def make_table(schedule, start_datetime=None):
    """ Given a list of session summaries, return a simple text table. """
    if start_datetime is None:
        start_datetime = datetime(1900, 1, 1)
    schedule_summary = [_session_summary(session) for session in schedule if \
            parser.parse(session.get('start', '2016')) > start_datetime]
    schedule_summary.sort(key=itemgetter('date', 'start_time', 'end_time'))
    return tabulate(schedule_summary, tablefmt="plain")
