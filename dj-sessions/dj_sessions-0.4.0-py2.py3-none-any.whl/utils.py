from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.timezone import now, timedelta

from .models import UserSession

DJ_CHANNELS_EXPIRE_DEFAULT = 12 * 3600  # 12 hours
DJ_CHANNELS_EXPIRE = getattr(
    settings,
    "DJ_CHANNELS_EXPIRE",
    DJ_CHANNELS_EXPIRE_DEFAULT
)


def remove_old_channel_sessions():
    """ Channel sessions are removed because these are set by websockets, and
        are recreated any time there is a socket disconnect (latency, server restart, browser refresh, etc). This assumes that the channel session is
        being set by the HTTP browser.

        :return int: Number of records removed.
    """
    sessions = Session.objects.filter(session_key__startswith='chn')
    sessions = sessions.filter(expire_date__lt=now())
    removed, data = sessions.delete()
    return removed

def remove_orphaned_sessions():
    """ Orphaned sessions are removed because sessions can be created multiple
        times per UserSession. This happens whenever there is a socket
        disconnect (latency, server restart, browser refresh, etc). This
        assumes that the channel session is being set by the HTTP browser.

        :return int: Number of records removed.
    """
    keys = UserSession.objects.values_list('session_key', flat=True)
    sessions = Session.objects.exclude(session_key__in=keys)
    removed, data = sessions.delete()
    return removed
