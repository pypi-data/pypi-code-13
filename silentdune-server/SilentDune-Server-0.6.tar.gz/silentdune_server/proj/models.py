#
# Authors: Robert Abram <robert.abram@entpack.com>,
#          Brett Donohoo <brett.donohoo@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


# Serialization Object for tuple lists.
class ChooserList(object):
    def __init__(self, pk, code, desc):
        self.pk = pk
        self.code = code
        self.desc = desc


# Generic record count class, used for serialization of record counts
class RecordCount (object):
    def __init__(self, count):
        self.data = {'count': count}


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WebLogTypes (BaseModel):

    wlt_code = models.CharField(max_length=20, unique=True)
    wlt_desc = models.CharField(_('Description'), max_length=250)
    wlt_container = models.CharField(_('Type Container'), max_length=250)
    wlt_retain_days = models.IntegerField(_('Retain Days'), default=365)

    class Meta:
        db_table = 'web_log_types'


class AbstractWebLog (BaseModel):

    wl_type = models.ForeignKey(WebLogTypes, related_name="%(class)s")
    user = models.IntegerField(_('User ID'), default=-1)
    wl_ipaddr = models.CharField(_('IP Address'), max_length=45)
    wl_content = models.CharField(_('Description'), max_length=1000)
    wl_action_flag = models.CharField(_('Action Flag'), max_length=1)

    class Meta:
        abstract = True


class WebLog (AbstractWebLog):

    class Meta:
        db_table = 'web_log'


class WebLogView (AbstractWebLog):

    wlt_code = models.CharField(max_length=10)
    wlt_desc = models.CharField(max_length=250)
    wlt_container = models.CharField(max_length=250)
    wlt_retain_days = models.IntegerField(default=365)

    class Meta:
        managed = False
        db_table = 'web_log_v'


class GlobalPreferences(models.Model):

    lockdown_slot_level = models.SmallIntegerField(_('Lockdown Slot Level'), default=160)
    polling_interval = models.PositiveIntegerField(_('Polling Interval'), default=60)
    
    class Meta:
        db_table = 'global_preferences'
        

#
# Log user actions into the web_log table.
# See proj/migrations/web_log_types.py for "Log Type" records and to add new types
#
# Example: activity_logger(request.user.id, 'LOGIN', ipaddr=get_client_ip(request))
#
def activity_logger(request=None, logcode='UNKNOWN', content='', action_flag='', user_id=None):

    # If we don't have a user id, don't bother logging
    if request is None and user_id is None:
        return

    # Test request for being an integer
    try:
        request += 1
        return
    except TypeError:
        pass

    if user_id is None:
        if request is not None and request.user.id is None:
            return

        user_id = request.user.id

    log = WebLog(user=user_id, wl_ipaddr=get_client_ip(request), wl_content=content, wl_action_flag=action_flag)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.error('Error: Unknown user id ({0}).'.format(user_id))

    try:
        logtype = WebLogTypes.objects.get(wlt_code=logcode)
    except WebLogTypes.DoesNotExist:
        logger.error('Error: Unknown WebLogTypes code used ({0}).'.format(logcode))
        return

    log.wl_type = logtype
    log.save()


def get_client_ip(request):

    if request is None:
        return ''

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


#
# Signals
#
def sig_user_logged_in(sender, user, request, **kwargs):

    activity_logger(request, 'LOGIN')


def sig_user_logged_out(sender, user, request, **kwargs):

    activity_logger(request, 'LOGOUT')


def sig_user_login_failed(sender, **kwargs):

    # Using django-axes to manage lockout after failed attempts.
    # This is just to log the event in our web_log table.

    uname = kwargs['credentials']['username']

    # Try to match up with an existing user record
    try:
        user = User.objects.get(username=uname)
    except User.DoesNotExist:
        activity_logger(-1, 'LOGIN_FAIL', content='user: unknown')
    else:
        activity_logger(user.id, 'LOGIN_FAIL', content='user:%s' % (uname))

#
# Connect signals to functions
#
user_logged_in.connect(sig_user_logged_in)
user_logged_out.connect(sig_user_logged_out)
user_login_failed.connect(sig_user_login_failed)
