# -*- coding: utf-8 -*-
"""
Similarly, this sending module is to represent the json templates that should
be used when sending something back to the user based on Facebook reference:

https://developers.facebook.com/docs/messenger-platform/send-api-reference

## CommonSender

`CommonSender` defines 4 attributes: `recipient`, `sender_action`,
`notification_type`, `message` because that's what [Facebook Send API](https://developers.facebook.com/docs/messenger-platform/send-api-reference) requires

And `send()` method actually sends the json string (serialized from the above
4 attributes) to Facebook endpoint using `requests` module

Each sender will definitely get psid as its first constructor argument. You can
define your own sender to provide customized behavior and then use it in the
routing policy

## Provided Senders

### ButtonSender (TBD)

### DefaultSender

Simple sends back the text defined in `DJM_DEFAULT_SENDER_TEXT`

- args: takes no argument

### MultimediaSender

Sends back a `SendingType` with its url

    ```
    image
    audio
    video
    file
    ```

- args:
    - sending_type: image, audio, video, file
    - url: url to the resource

### QuickReplySender (TBD)

### SenderActionSender

Sends back a sender action, check [Facebook Reference](https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions)

- args:
    - action: mark_seen, typing_on, typing_off

### SimpleMessageSender

Sends back a simple text message, could be i18n'ed

- args:
    - text: message to send back to user

"""
import requests
from abc import abstractmethod
import logging
import gettext

from djmessenger.utils.serializable import SerializableEnum, Serializable
from djmessenger.receiving import Recipient
from djmessenger.settings import DJM_POST_MESSAGE_URL, DJM_DEFAULT_SENDER_TEXT, DJM_BOT_PREFIX
from djmessenger.models import Sending, FBUserProfile
# from django.utils.translation import ugettext_lazy as _
from djmessenger.utils.i18n import *


logger = logging.getLogger(__name__)


class SendingType(SerializableEnum):
    pass


SendingType.SIMPLE_TEXT = SendingType('simple_text')
SendingType.QUICK_REPLY = SendingType('quick_reply')
SendingType.BUTTON = SendingType('button')
SendingType.IMAGE = SendingType('image')
SendingType.AUDIO = SendingType('audio')
SendingType.VIDEO = SendingType('video')
SendingType.FILE = SendingType('file')
SendingType.SENDER_ACTION = SendingType('sender_action')


class NotificationType(SerializableEnum):
    pass


NotificationType.REGULAR = NotificationType('REGULAR')
NotificationType.SILEN_PUSH = NotificationType('SILEN_PUSH')
NotificationType.NO_PUSH = NotificationType('NO_PUSH')


class SenderAction(SerializableEnum):
    pass


SenderAction.MARK_SEEN = SenderAction('mark_seen')
SenderAction.TYPING_ON = SenderAction('typing_on')
SenderAction.TYPING_OFF = SenderAction('typing_off')


class CommonSender(Serializable):
    includes = ('recipient', 'sender_action', 'notification_type', 'message')

    def __init__(self, psid, sender_action=None,
                 notification_type=NotificationType.REGULAR.name):
        """
        Define highest level of sending template

        @param psid: the user you'd like to send this to, this psid must be
                     obtained from receiving message
        @type psid: str

        @param sender_action: sender action
        @type sender_action: SenderAction

        @param notification_type: mostly no need to change this, default is
                                  regular
        @type notification_type: NotificationType
        """
        self.recipient = Recipient(psid)
        self.sender_action = sender_action
        self.notification_type = notification_type
        self.message = None

    @abstractmethod
    def get_message(self):
        """
        Based on the attributes the class constructor constructs, this method
        returns the message body, the returned must be a dict and valid json
        object

        @return:
        @rtype: dict
        """
        pass

    def send(self):
        self.message = self.get_message()
        data = self.json()
        logger.debug('Sending %s message to user %s: %s' %
                     (self.get_sending_type(), self.recipient.id, data))
        status = requests.post(DJM_POST_MESSAGE_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        try:
            recipient = FBUserProfile.objects.get(pk=self.recipient.id)
            try:
                sending = Sending.objects.create(recipient=recipient, data=data,
                                                 type=self.get_sending_type().name)
                sending.response = status.content
                sending.status_code = status.status_code
                sending.save()
            except Exception as e:
                logger.debug('Failed to create Sending object because %s' % e)
        except FBUserProfile.DoesNotExist:
            logger.debug('Recipient PSID not found in database table djm_user,'
                         ' since PSID was not found, not able to save what are '
                         'we sending')

    @abstractmethod
    def get_sending_type(self):
        """
        Return the SendingType that this Sender sends

        @return:
        @rtype: SendingType
        """
        pass

    @classmethod
    def preprocess_outgoing_string(cls, psid, text):
        """This method take cares of any preprocessing of the outgoing text

        @param psid:
        @param text:
        @return:
        """
        install_user_locale(psid)
        try:
            ret = _(DJM_BOT_PREFIX).encode('utf-8') + _(text).encode('utf-8')
        except:
            # if the locale is not supported, _() will fail, so catch it and
            # fallback to English
            ret = DJM_BOT_PREFIX.encode('utf-8') + text.encode('utf-8')
        reset_locale()
        return ret

    def get_psid(self):
        return self.recipient.id


class SenderActionSender(CommonSender):
    """
    Send a Sender Action
    """
    def __init__(self, psid, action):
        super().__init__(psid, action)

    def get_sending_type(self):
        return SendingType.SENDER_ACTION

    def get_message(self):
        # no message
        return ""


class SimpleMessageSender(CommonSender):
    """
    Send a simple text message
    """
    def __init__(self, psid, text):
        super().__init__(psid)
        self.text = text

    def get_message(self):
        # FUTURE: we can probably move this part to CommonSender so that
        #         subclasses don't need to worry about it
        text = CommonSender.preprocess_outgoing_string(
            self.get_psid(), self.text)
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        return {"text": text}

    def get_sending_type(self):
        return SendingType.SIMPLE_TEXT


class DefaultSender(SimpleMessageSender):
    """
    Sends back simple text DJM_DEFAULT_SENDER_TEXT
    """
    def __init__(self, psid):
        super().__init__(psid, DJM_DEFAULT_SENDER_TEXT)


class MultimediaSender(CommonSender):
    # TODO: should work with django static???
    """
    Send back multimedia from a url

    SendingType.IMAGE = SendingType('IMAGE')
    SendingType.AUDIO = SendingType('AUDIO')
    SendingType.VIDEO = SendingType('VIDEO')
    SendingType.FILE = SendingType('FILE')
    """

    def __init__(self, psid, sending_type, url):
        super().__init__(psid)
        self.sending_type = sending_type
        self.url = url

    def get_sending_type(self):
        return SendingType.value_of(self.sending_type)

    def get_message(self):
        return {"attachment": {
            "type": self.get_sending_type().name.lower(),
            "payload": {
                "url": self.url
            }
        }}

class ButtonSender(CommonSender):
    # TODO:
    pass


class QuickReplySender(CommonSender):
    # TODO:
    pass
