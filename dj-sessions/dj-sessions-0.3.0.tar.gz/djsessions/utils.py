from django.contrib.sessions.models import Session
from django.utils.timezone import now, timedelta


def remove_old_channel_sessions():
    """ Channel sesssions are removed because these are set by websockets, and
        are recreated any time there is a socket disconnect (latency, server restart, browser refresh, etc). This assumes that the channel session is
        being set by the HTTP browser.

        :return int: Number of records removed.
    """
    sessions = Session.objects.filter(session_key__startswith='chn')
    sessions = sessions.filter(expire_date__lt=now())
    removed, data = sessions.delete()
    return removed
