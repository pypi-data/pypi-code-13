# -*- coding: utf-8 -*-
import datetime

from django.utils.tzinfo import LocalTimezone
from django.utils.translation import ungettext, ugettext as _


def timesince(d, now=None):

    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        if d.tzinfo:
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now()

    today = datetime.datetime(now.year, now.month, now.day)

    delta = now - d

    delta_midnight = today - d
    days = delta.days
    hours = int(round(delta.seconds / 3600., 0))
    minutes = int(round(delta.seconds / 60., 0))

    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n : ungettext('week', 'weeks', n)),
        (1.0, lambda n : ungettext('day', 'days', n)),
    )

    if days == 0:
        if hours == 0:
            if minutes > 0:
                return ungettext('%(minutes)d minute ago', \
                                 '%(minutes)d minutes ago', minutes) % \
                            {'minutes': minutes}
            else:
                seconds = delta.seconds if delta.seconds > 10 else 10
                return ungettext('%(seconds)d second ago',
                                 '%(seconds)d seconds ago', seconds) % \
                            {'seconds': seconds}
        else:
            return ungettext('%(hours)d hour ago',
                             '%(hours)d hours ago', hours) % {'hours':hours}

    if delta_midnight.days == 0:
        return _("yesterday at %s") % d.strftime("%H:%M")

    count = 0
    for i, (chunk, name) in enumerate(chunks):
        if days >= chunk:
            count = round((delta_midnight.days + 1)/chunk, 0)
            break

    return _('%(number)d %(type)s ago') % {'number': count, 'type': name(count)}
