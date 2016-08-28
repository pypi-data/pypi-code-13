# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _
from djmessenger.utils.default_routing_policy import DJM_DEFAULT_ROUTING_POLICY


DJM_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Facebook Page Access Token, get it from developers.facebook.com
DJM_PAGE_ACCESS_TOKEN = getattr(settings, 'DJM_PAGE_ACCESS_TOKEN', '')

# The endpoint that Facebook will relay the callback message to
# also being used to setup webhook
DJM_ENDPOINT = getattr(settings, 'DJM_ENDPOINT', '')

# Whether DJM should automatically fetch and save user profile for any user that
# sends message to the page and observed by BOT, default to True
DJM_SAVE_USER_PROFILE = getattr(settings, 'DJM_SAVE_USER_PROFILE', True)

# You probably don't need to change this
DJM_POST_MESSAGE_URL = getattr(settings, 'DJM_POST_MESSAGE_URL',
                               'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % DJM_PAGE_ACCESS_TOKEN)

# You probably don't need to change this
DJM_USER_DETAILS_URL = getattr(settings, 'DJM_USER_DETAILS_URL',
                               'https://graph.facebook.com/v2.6/%s')

# You probably don't need to change this
DJM_THREAD_SETTINGS_URL = getattr(settings, 'DJM_THREAD_SETTINGS_URL',
                                  'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s' % DJM_PAGE_ACCESS_TOKEN)

# A sender named djmessenger.sending.DefaultSender which is a SimpleTextSender
# you can define your message here and directly use it in DJM_ROUTING_POLICY
DJM_DEFAULT_SENDER_TEXT = getattr(settings, 'DJM_DEFAULT_SENDER_TEXT',
                                  _('Thanks for your message'))

# Prefix this string to all text messages sent to users
DJM_BOT_PREFIX = getattr(settings, 'DJM_BOT_PREFIX', _("BOT: "))

"""
## DJM_ROUTING_POLICY

DJM_ROUTING_POLICY defines the lifecycle of a message being received, handling
it and lastly send some response back. In the following format, each router
represents a type of message received, handlers represent which handlers should
be used to handle this type of message and lastly which senders should be used
to send the response back.

DEFAULT is a special type, it is not a type that Facebok would send over but it
is merely for DJM to know that the handlers listed in DEFAULT should apply to
all other types as well.

For example, in the following default policy, router[1], it basically means

1. If we got a message type is sticker
2. send the message to ThumbUpHandler
3. ThumbUpHandler.should_handle() will check whether it is valid to handle this
   message, if yes, handle it
4. Then senders defines which Sender class should be used to send something back
"""
DJM_ROUTING_POLICY = getattr(settings, 'DJM_ROUTING_POLICY',
                             DJM_DEFAULT_ROUTING_POLICY)

# prechecks
if not DJM_PAGE_ACCESS_TOKEN or not DJM_ENDPOINT:
    raise ImproperlyConfigured(
        _('djmessenger requires at least DJM_PAGE_ACCESS_TOKEN and DJM_ENDPOINT'
          ' to be configured in your settings.py')
    )
