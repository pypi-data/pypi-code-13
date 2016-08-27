# -*- coding: utf-8 -*-
"""
When BOT receives a message and constructed Callback object, use handler to
handler different types of message
"""
from abc import ABC, abstractmethod
from djmessenger.receiving import Messaging, ReceivingType
import logging
import requests
from djmessenger.models import UserLocation, FBUserProfile
from django.utils.translation import ugettext_lazy as _
import json
from .sending import DefaultSender, SimpleMessageSender, MultimediaSender, SendingType
from .settings import DJM_SAVE_MESSAGING


logger = logging.getLogger(__name__)


class BaseHandler(ABC):
    """
    BaseHandler is an abstract base class to

    1. Determine whether the given messaging object should be handled by this
       handler
    2. Actually handle it by adding something to database, or other internal
       work and eventually sending something back using sending module

    Each received messaging object will be applied to all defined handlers,
    which means you can actually do multiple stuff for a single messaging as
    long as your should_handle returns True
    """
    def __init__(self, messaging):
        """

        @param messaging:
        @type messaging: Messaging
        """
        self.messaging = messaging

    def get_psid(self):
        return self.messaging.get_psid()

    @abstractmethod
    def should_handle(self):
        """
        Whether the given messaging is applicable for this handler

        @return: True if the messaging should be handled; False otherwise
        @rtype: bool
        """
        pass

    @abstractmethod
    def handle(self):
        """
        Actually handles the messaging

        @return:
        """
        pass


class SaveMessagingHandler(BaseHandler):
    def should_handle(self):
        return DJM_SAVE_MESSAGING

    def handle(self):
        logger.debug('Handling saving messaging...')
        from djmessenger.models import Messaging as ModelMessaging
        ModelMessaging.objects.create(body=self.messaging.serialize(),
                                      type=self.messaging.get_receiving_type())


class UserProfileHandler(BaseHandler):
    """
    Every messaging has sender.id, based on settings.DJM_SAVE_USER_PROFILE, this
    handler save user profile into database using models.FBUserProfile.

    If DJM_SAVE_USER_PROFILE was True, we fetch user profile using graph API;
    otherwise we only save user psid to the database
    """
    def should_handle(self):
        return True

    def handle(self):
        from djmessenger.models import FBUserProfile
        from djmessenger.settings import DJM_USER_DETAILS_URL, DJM_PAGE_ACCESS_TOKEN, DJM_SAVE_USER_PROFILE

        # we already checked this id exists in should_handle
        psid = self.get_psid()
        logger.debug('Handling user %s' % psid)
        try:
            FBUserProfile.objects.get(pk=psid)
            # user already exists
            logger.debug('PSID %s already exists, no need to fetch' % psid)
        except FBUserProfile.DoesNotExist:
            logger.debug('User %s does not exist, trying to create' % psid)
            if DJM_SAVE_USER_PROFILE:
                # user does not exist
                logger.debug('Ready to fetch and save user details for PSID %s' %
                             psid)
                status = requests.get(
                    DJM_USER_DETAILS_URL % psid,
                    {'access_token': DJM_PAGE_ACCESS_TOKEN}
                )
                if status.status_code != 200:
                    logger.error('Failed to fetch user details using Facebook Graph'
                                 'API for PSID %s' % psid)
                else:
                    user_detail = status.json()
                    logger.debug('Successfully fetched user profile for psid %s'
                                 ': %s'
                                 % (psid, user_detail))
                    try:
                        fp = FBUserProfile(**user_detail)
                        fp.psid = psid
                        fp.save()
                        logger.debug('Successfully handled creating user '
                                     'profile for %s' % psid)
                    except:
                        logger.debug('Failed to create FBUserProfile from user'
                                     'details: %s' % user_detail)
            else:
                # do not fetch user profile, only save psid
                FBUserProfile.objects.create(psid=psid)


class LocationHandler(BaseHandler):
    """
    If the user sends a location to the BOT (by click on the map pin icon next
    to thumb up), this handler saves this coordinates to the database
    """
    def should_handle(self):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = self.messaging.get_receiving_type() == ReceivingType.LOCATION
        logger.debug('We check whether the messaging callback type is '
                     'MESSAGE_RECEIVED_LOCATION. The result is %s' % ret)
        return ret

    def handle(self):
        message = self.messaging.message
        psid = self.get_psid()
        try:
            user = FBUserProfile.objects.get(pk=psid)
            timestamp = self.messaging.timestamp if hasattr(self.messaging,
                                                            'timestamp') else None
            for atta in self.messaging.message.attachments:
                if not atta.type == 'location':
                    continue
                location = UserLocation(user=user,
                                        latitude=atta.payload.coordinates.lat,
                                        longitude=atta.payload.coordinates.long,
                                        timestamp=timestamp,
                                        mid=self.messaging.message.mid,
                                        seq=self.messaging.message.seq,
                                        url=getattr(atta, 'url', None)
                                        )
                location.save()
            logger.debug(
                'Successfully handled message containing location sent '
                'from %s' % psid)
        except FBUserProfile.DoesNotExist:
            logger.debug('No profile for psid %s, it is probably because'
                         'UserProfileHandler was not enabled.' % psid)


class ThumbUpHandler(BaseHandler):
    """
    Handles when the user sends a thumb up
    """
    def should_handle(self):
        logger.debug('Ready to determine whether %s should handle this '
                     'messaging' % self.__class__.__name__)
        ret = self.messaging.get_receiving_type() == ReceivingType.STICKER \
            and str(self.messaging.get_sticker_id())[-3:] in ('810', '814', '822')
        logger.debug('We determine whether we should handle the messaging by '
                     '1. check if the callback type is MESSAGE_RECEIVED_STICKER'
                     ', 2. check if the last 3 digit of sticker id is either '
                     '810, 814 or 822. The result is %s' % ret)
        return ret

    def handle(self):
        psid = self.get_psid()
        logger.debug('Handling Thumbup from %s' % psid)
        try:
            user = FBUserProfile.objects.get(pk=psid)
            user.thumbups += 1
            user.save()
        except FBUserProfile.DoesNotExist:
            logger.debug('No profile for psid %s, it is probably because'
                         'UserProfileHandler was not enabled.' % psid)
        # sending
        # SimpleMessageSender(psid, _('Thank you for your thumb!!!')).send()
        # MultimediaSender(psid, SendingType.IMAGE, 'https://dl.dropboxusercontent.com/u/717667/carsend_logo.jpg').send()

# TODO: how to handle postback?
class PayloadHandler(BaseHandler):
    SENDER_KEY_NAME = '_sender'

    """
    Postback and QuickReply contains payload, and in order to support request
    chaining, we need to provide a default base class for Postback and
    QuickReply.

    Since the payload in Postback and QuickReply is merely a simple string
    limited to 1000 chars, we can utilize this space to send some bookkeeping
    info to achieve request chaining.

    We are going to make the payload (which is a plain text) looks like a valid
    json object so that we can deserialize it back to a dict and then we can
    figure out which handler was the sender, then do corresponding actions
    """

    @abstractmethod
    def get_payload(self):
        """

        @return: the corresponding payload string
        @rtype: str
        """
        pass


class PostbackBaseHandler(PayloadHandler):

    def should_handle(self):
        return self.messaging.get_receiving_type() == ReceivingType.POSTBACK

    def get_payload(self):
        return self.messaging.get_postback_payload()


class QuickReplyBaseHandler(PayloadHandler):

    def should_handle(self):
        return self.messaging.get_receiving_type() == ReceivingType.QUICK_REPLY

    def get_payload(self):
        return self.messaging.get_quick_reply_payload()

    def get_text(self):
        """
        quick reply will come with text which is the quick reply title

        @return:
        """
        return self.messaging.get_text()


class SimpleTextBaseHandler(BaseHandler):
    def __init__(self, messaging, text=None, regex=None):
        super().__init__(messaging)
        self.regex = regex
        self.text = text

    def should_handle(self):
        from re import compile

        if not self.regex:
            return len(self.messaging.get_text()) > 0
        rex = compile(self.regex)
        res = rex.fullmatch(self.get_text())
        return res and len(self.messaging.get_text()) > 0

    def get_text(self):
        return self.messaging.get_text()

    def handle(self):
        SimpleMessageSender(self.get_psid(), _(self.text))
