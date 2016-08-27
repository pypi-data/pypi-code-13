# -*- coding: utf-8 -*-
from django.db import models
from .utils.serializable import Serializable
from django.utils.translation import ugettext_lazy as _
from .exceptions import DJMInvalidConfigException
import requests
import logging


logger = logging.getLogger(__name__)


class Messaging(models.Model):
    body = models.TextField()
    type = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'djm_messaging'


class Sending(models.Model):
    recipient = models.ForeignKey('FBUserProfile')
    date_sent = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    type = models.CharField(max_length=128, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'djm_sending'


class FBUserProfile(models.Model):
    """
    This FacebookUser class is to represent a user that sent a message to us
    via Facebook Messenger, from the message relayed by Facebook, we can look
    up user details which will be stored here
    """
    psid = models.CharField(max_length=512, primary_key=True)
    first_name = models.CharField('first name', max_length=512, null=True,
                                  blank=True)
    last_name = models.CharField('last name', max_length=512, null=True,
                                 blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    locale = models.CharField(max_length=128, null=True, blank=True)
    timezone = models.SmallIntegerField()
    gender = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    thumbups = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'djm_user'


class UserLocation(models.Model):
    """
    From the message user sent via Facebook to us, addition to saving the raw
    request body into RawBody, we try to see if the sent message is actually a
    location that contains lat and long, if yes, then we save it here
    """
    user = models.ForeignKey(FBUserProfile, null=False, blank=False)
    latitude = models.DecimalField(max_digits=10,
                                   decimal_places=8,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=11,
                                    decimal_places=8,
                                    null=True, blank=True)
    timestamp = models.BigIntegerField(
        help_text='Facebook returns timestamp as EPOCH')
    url = models.URLField(max_length=1000, null=True, blank=True)
    mid = models.CharField(max_length=512, null=True, blank=True)
    seq = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.date_created = datetime.utcnow().replace(tzinfo=utc)
    #     super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'date_created'
        db_table = 'djm_userlocation'

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%s(%s, %s)' % (self.user, self.latitude, self.longitude)


class Greetings(models.Model):
    text = models.CharField(
        max_length=160,
        unique=True,
        null=False,
        blank=False,
        primary_key=True,
        help_text=_('This is the greeting text your user will see when the user'
                    'interacts with your page in the first time on Messenger'
                    '. You can only configure 1 of this, text length limit is'
                    '160 chars.'))

    def save(self, *args, **kwargs):
        if Greetings.objects.count() > 0:
            raise DJMInvalidConfigException(
                _('Facebook regulated that greeting text can have only 1, it'
                  'seems you are trying to add more than 1'))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'djm_greetings'


class GetStartedButton(models.Model):
    """
    The Get Started button is only rendered the first time the user interacts
    with a the Page on Messenger.
    """
    payload = models.CharField(
        max_length=160,
        unique=True,
        null=False,
        blank=False,
        primary_key=True,
        help_text=_('The payload string will be sent back to you via Postback,'
                    'so once you added a Get Started Button here, you also '
                    'need to define how to handle the payload'))

    def save(self, *args, **kwargs):
        if GetStartedButton.objects.count() > 0:
            raise DJMInvalidConfigException(
                _('Facebook regulated that get started button can have only 1, '
                  'it seems you are trying to add more than 1'))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'djm_getstarted'


class PersistentMenu(models.Model, Serializable):
    """
    The Persistent Menu is a menu that is always available to the user.
    This menu should contain top-level actions that users can enact at any
    point. Having a persistent menu easily communicates the basic capabilities
    of your bot for first-time and returning users.
    The menu can be invoked by a user, by tapping on the 3-caret icon on the
    left of the composer.
    """
    MENU_TYPE_CHOICES = (
        ('postback', _('postback')),
        ('web_url', _('web_url'))
    )
    type = models.CharField(
        max_length=10, choices=MENU_TYPE_CHOICES, default='web_url',
        help_text=_('postback means when clicking on the menu, it will send '
                    'the payload back to the server; while web_url simply opens'
                    ' the url'))
    title = models.CharField(max_length=30, null=False, blank=False, unique=True
                             , help_text=_('Button title, case sensitive, '
                                           'unique'))
    url = models.URLField(
        help_text=_('For web_url buttons, this URL is opened in a mobile '
                    'browser when the button is tapped')
    )
    payload = models.CharField(
        max_length=1000,
        help_text=_('For postback buttons, this data will be sent back to you '
                    'via webhook')
    )

    def save(self, *args, **kwargs):
        if PersistentMenu.objects.count() == 5:
            raise DJMInvalidConfigException(
                _('Facebook regulated that get started button can have only 5, '
                  'it seems you are trying to add more than 1'))
        if self.type == 'postback' and not self.payload:
            raise ValueError(_('If persistent menu type is postback, you need'
                               ' to configure payload as well'))
        if self.type == 'web_url' and not self.url:
            raise ValueError(_('If persisent menu type is web_url, you need to '
                               'configure url as well'))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'djm_persistentmenu'

    def json(self):
        if self.type == 'postback':
            return {
                'type': self.type,
                'title': self.title,
                'payload': self.payload
            }
        elif self.type == 'web_url':
            return {
                'type': self.type,
                'title': self.title,
                'url': self.url
            }
