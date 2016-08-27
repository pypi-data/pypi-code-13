# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _

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
# whether you want to save the entire request body as a json string in the database
DJM_SAVE_MESSAGING = getattr(settings, 'DJM_SAVE_MESSAGING', False)
DJM_SUPERUSER_USERNAME = getattr(settings, 'DJM_SUPERUSER_USERNAME', 'admin')
DJM_SUPERUSER_PASSWORD = getattr(settings, 'DJM_SUPERUSER_USERNAME', 'Admin!23')
DJM_SUPERUSER_EMAIL = getattr(settings, 'DJM_SUPERUSER_EMAIL', 'admin@abc.com')
DJM_DEFAULT_SENDER = getattr(settings, 'DJM_DEFAULT_SENDER',
                             'djmessenger.sender.DefaultSender')
DJM_DEFAULT_SENDER_TEXT = getattr(settings, 'DJM_DEFAULT_SENDER_TEXT',
                                  _('Thanks for your message'))
DJM_ROUTING_POLICY = getattr(
    settings,
    'DJM_ROUTING_POLICY',
    {
        "routers": [
            {
                "type": "DEFAULT",
                "handlers": [
                    {
                        "name": "djmessenger.handling.SaveMessagingHandler",
                        "args": [],
                        "senders": []
                    },
                    {
                        "name": "djmessenger.handling.UserProfileHandler",
                        "args": [],
                        "senders": []
                    }
                ]
            },
            {
                "type": "STICKER",
                "handlers": [
                    {
                        "name": "djmessenger.handling.ThumbUpHandler",
                        "args": [],
                        "senders": [
                            {
                                "name": "djmessenger.sending.SimpleMessageSender",
                                "args": [
                                    _("Thank you for your thumb!!!")
                                ]
                            },
                            {
                                "name": "djmessenger.sending.MultimediaSender",
                                "args": [
                                    "image",
                                    "https://dl.dropboxusercontent.com/u/717667/carsend_logo.jpg"
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "SIMPLE_TEXT",
                "handlers": [
                    {
                        "name": "djmessenger.handling.SimpleTextBaseHandler",
                        "args": [],
                        "senders": [
                            {
                                "name": "djmessenger.sending.SimpleMessageSender",
                                "args": [
                                    _("Thanks for your message, we will get back to you soon")
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "LOCATION",
                "handlers": [
                    {
                        "name": "djmessenger.handling.LocationHandler",
                        "args": [],
                        "senders": []
                    }
                ]
            }
        ]
    }

)

# prechecks
if not DJM_PAGE_ACCESS_TOKEN or not DJM_ENDPOINT:
    raise ImproperlyConfigured(
        _('djmessenger requires at least DJM_PAGE_ACCESS_TOKEN and DJM_ENDPOINT'
          ' to be configured in your settings.py')
    )
