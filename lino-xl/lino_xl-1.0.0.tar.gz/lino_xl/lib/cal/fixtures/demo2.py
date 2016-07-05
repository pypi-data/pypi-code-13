# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
#
# This file is part of Lino XL.
#
# Lino XL is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino XL is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino XL.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Generates a suite of fictive demo events.
"""

import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)
DEMO_DURATION = relativedelta(hours=1, minutes=30)

from django.conf import settings
from django.utils.translation import ugettext as _

from lino.utils import Cycler

from lino.api import dd, rt

cal = dd.resolve_app('cal')
Event = dd.resolve_model('cal.Event')
EventType = dd.resolve_model('cal.EventType')
# Subscription = rt.modules.cal.Subscription
Calendar = dd.resolve_model('cal.Calendar')


# def subscribe_all():

#     for u in settings.SITE.user_model.objects.exclude(profile=''):
#         for obj in Calendar.objects.all():
#             obj = Subscription(user=u, calendar=obj)
#             yield obj


def objects():

    #~ if settings.SITE.project_model:
        #~ PROJECTS = Cycler(settings.SITE.project_model.objects.all())
    ETYPES = Cycler(EventType.objects.filter(is_appointment=True))

    def s2duration(s):
        h, m = map(int, s.split(':'))
        #~ return relativedelta(hours=h,minutes=m)
        return datetime.timedelta(hours=h, minutes=m)

    def s2time(s):
        h, m = map(int, s.split(':'))
        return datetime.time(h, m)
    TIMES = Cycler([s2time(s)
                   for s in ('08:30', '09:40', '10:20', '11:10', '13:30')])
    #~ DURATIONS = Cycler([s2duration(s) for s in ('00:30','00:40','1:00','1:30','2:00','3:00')])
    DURATIONS = Cycler([s2duration(s)
                       for s in ('01:00', '01:15', '1:30', '1:45', '2:00', '2:30', '3:00')])
    ACL = Cycler(cal.AccessClasses.items())
    STATES = Cycler(cal.EventStates.items())
    SUMMARIES = Cycler((
        dict(en='Lunch', de=u"Mittagessen", fr=u"Diner"),
        dict(en='Dinner', de=u"Abendessen", fr=u"Souper"),
        dict(en='Breakfast', de=u"Frühstück", fr=u"Petit-déjeuner"),
        dict(en='Meeting', de=u"Treffen", fr=u"Rencontre"),
        dict(en='Consultation', de=u"Beratung", fr=u"Consultation"),
        dict(en='Seminar', de=u"Seminar", fr=u"Séminaire"),
        dict(en='Evaluation', de=u"Auswertung", fr=u"Evaluation"),
        dict(en='First meeting', de=u"Erstgespräch", fr=u"Première rencontre"),
        dict(en='Interview', de=u"Interview", fr=u"Interview")
    ))
    #~ for i in range(20):

    for u in settings.SITE.user_model.objects.exclude(email=''):
        #~ u = USERS.pop()
        if True:
            date = settings.SITE.demo_date()
            for i in range(12):
                if i % 3:
                    date += ONE_DAY  # relativedelta(days=1)
                s = SUMMARIES.pop().get(
                    u.language, None) or SUMMARIES.pop().get('en')
                st = TIMES.pop()
                kw = dict(user=u,
                          start_date=date,
                          event_type=ETYPES.pop(),
                          start_time=st,
                          summary=s)
                kw.update(access_class=ACL.pop())
                kw.update(state=STATES.pop())
                #~ if settings.SITE.project_model:
                    #~ kw.update(project=PROJECTS.pop())
                e = Event(**kw)
                e.set_datetime('end', e.get_datetime('start')
                               + DURATIONS.pop())
                yield e

    # # some conflicting events
    # USERS = Cycler(rt.users.User.objects.all())
    # ET = EventType.objects.filter(is_appointment=True)
    # date = settings.SITE.demo_date(200)
    # e = Event(start_date=date, summary="Conflicting 1", event_type=ETYPES.pop(), user=USERS.pop())
    # yield e
