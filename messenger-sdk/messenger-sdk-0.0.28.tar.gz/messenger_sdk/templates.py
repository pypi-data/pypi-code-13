from abc import abstractmethod
from abc import ABCMeta

# class BaseTemplate:
#     def __init__(self, recipient_id, quick_replies=None, metadata=None):
#         self.recipient_id = recipient_id
#         self._quick_replies = quick_replies
#         self._metadata = metadata
#
#     @abstractmethod
#     def __dict__(self):
#         raise NotImplementedError()
#
#
# class PlainTextMessage(BaseTemplate):
#     def __init__(self, recipient_id, text, quick_replies=None, metadata=None):
#         super().__init__(recipient_id=recipient_id,
#                          quick_replies=quick_replies,
#                          metadata=metadata)
#         self.text = text
#
#     def __dict__(self):
#         return {
#             'recipient': {
#                 'id': self.recipient_id
#             },
#             'message': {
#                 'text': self.text
#             }
#         }
#
#
# class ButtonMessage(BaseTemplate):
#     def __init__(self, recipient_id, text, buttons, quick_replies=None, metadata=None):
#         super().__init__(recipient_id=recipient_id,
#                          quick_replies=quick_replies,
#                          metadata=metadata)
#         self.text = text
#         self.buttons = buttons
#
#     def __dict__(self):
#         return {
#             'recipient': {
#                 'id': self.recipient_id
#             },
#             'message': {
#                 'attachment': {
#                     'type': 'template',
#                     'payload': {
#                         'template_type': 'button',
#                         'text': self.text,
#                         'buttons': [button.__dict__() for button in self.buttons]
#                     }
#                 }
#             }
#         }
#
#
# class Button:
#     def __init__(self, title, type='postback', url=None, payload=None):
#         self._title = title
#         self._url = None
#         self._payload = None
#
#         if type in ['postback', 'web_url']:
#             self._type = type
#         else:
#             raise ValueError("Type must be postback or web_url.")
#
#         if type == 'web_url':
#             if url is not None:
#                 self._url = url
#             else:
#                 raise ValueError("Url is required with web_url type.")
#
#         if type == 'postback':
#             if payload is not None:
#                 self._payload = payload
#             else:
#                 raise ValueError("Payload is required with postback type.")
#
#     @property
#     def title(self):
#         return self._title
#
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def url(self):
#         return self._url
#
#     @property
#     def payload(self):
#         return self._payload
#
#     def __dict__(self):
#         item = {
#             'type': self.type,
#             'title': self.title
#         }
#         if self.url:
#             item['url'] = self.url,
#         if self.payload:
#             item['payload'] = self.payload
#
#         return item
#
#
# class GenericMessage(BaseTemplate):
#     def __init__(self, recipient_id, elements):
#         self.recipient_id = recipient_id
#         if len(elements) > 10:
#             raise ValueError("Max number of elements is 10.")
#         self.elements = elements
#
#     def __dict__(self):
#         return {
#             'recipient': {
#                 'id': self.recipient_id
#             },
#             'message': {
#                 'attachment': {
#                     'type': 'template',
#                     'payload': {
#                         'template_type': 'generic',
#                         'elements': [e.__dict__() for e in self.elements]
#                     }
#                 }
#             }
#         }
#
#
# class Element:
#     def __init__(self, title, item_url=None, image_url=None, subtitle=None, buttons=None):
#         self._title = title
#         self._item_url = None
#         self._image_url = None
#         self._subtitle = None
#         self._buttons = None
#
#         if subtitle:
#             self._subtitle = subtitle
#         if item_url:
#             self._item_url = item_url
#         if image_url:
#             self._image_url = image_url
#         if buttons:
#             if len(buttons) > 3:
#                 raise ValueError("Max number of buttons is 3.")
#             self._buttons = buttons
#
#     def __dict__(self):
#         item = {
#             'title': self.title,
#             'subtitle': self.subtitle,
#             'image_url': self.image_url,
#             'item_url': self.item_url
#         }
#         if self.buttons:
#             item['buttons'] = [b.__dict__() for b in self.buttons]
#
#         return item
#
#     @property
#     def title(self):
#         return self._title
#
#     @property
#     def item_url(self):
#         return self._item_url
#
#     @property
#     def image_url(self):
#         return self._image_url
#
#     @property
#     def subtitle(self):
#         return self._subtitle
#
#     @property
#     def buttons(self):
#         return self._buttons


class Response(metaclass=ABCMeta):
    _notification_types = ['REGULAR', 'SILENT_PUSH', 'NO_PUSH']
    NOTIFICATION_TYPE_REGULAR = 'REGULAR'
    NOTIFICATION_TYPE_SILENT_PUSH = 'SILENT_PUSH'
    NOTIFICATION_TYPE_NO_PUSH = 'NO_PUSH'

    _sender_actions = ['typing_on', 'typing_off', 'mark_seen']
    SENDER_ACTION_TYPING_ON = 'typing_on'
    SENDER_ACTION_TYPING_OFF = 'typing_off'
    SENDER_ACTION_MARK_SEEN = 'mark_seen'

    def __init__(self, recipient_id, notification_type=None, message=None, sender_action=None):
        self._recipient_id = recipient_id
        self._message = message
        self._sender_action = sender_action
        if not notification_type:
            notification_type = Response.NOTIFICATION_TYPE_REGULAR
        self._notification_type = notification_type

        self.throw_if_not_valid()

    def throw_if_not_valid(self):
        if not self.message and not self.sender_action:
            raise ValueError('message or sender_action must be set.')

        if self.sender_action.lower() and self.sender_action not in self._sender_actions:
            raise ValueError(
                'Invalid sender_action. Given: {given}. Expected: {expected}.'.format(given=self.sender_action,
                                                                                      expected=self._sender_actions))
        if self.notification_type.upper() not in self._notification_types:
            raise ValueError(
                'Invalid notification_type. Given: {given}. Expected: {expected}.'.format(given=self.notification_type,
                                                                                          expected=self._notification_types))
        if self.message and not isinstance(self.message, Message):
            raise TypeError(
                'Invalid message type. Expected {expected}, given {given}.'.format(expected=Message.__class__.__name__,
                                                                                   given=type(self.message).__name__))

    def __dict__(self):
        template = {
            'recipient': {
                'id': self.recipient_id
            },
            'notification_type': self.notification_type
        }
        if self.message:
            template.update({'message': self.message.__dict__()})
        if self.sender_action:
            self.sender_action({'sender_action': self.sender_action})

        return template

    @property
    def recipient_id(self):
        return self._recipient_id

    @property
    def message(self):
        return self._message

    @property
    def sender_action(self):
        return self._sender_action.lower()

    @property
    def notification_type(self):
        return self._notification_type.upper()


class TextResponse(Response):
    def __init__(self, recipient_id,
                 text,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        message = Message(text=text, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class GenericResponse(Response):
    def __init__(self, recipient_id,
                 elements: list,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        attachment = Attachment(type='template', payload=GenericPayload(elements=elements))
        message = Message(attachment=attachment, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class ButtonResponse(Response):
    def __init__(self, recipient_id,
                 text: str,
                 buttons: list,
                 notification_type=None,
                 quick_replies=None,
                 metadata=None):
        attachment = Attachment(type='template', payload=ButtonPayload(buttons=buttons, text=text))
        message = Message(attachment=attachment, quick_replies=quick_replies, metadata=metadata)
        super().__init__(recipient_id=recipient_id, notification_type=notification_type, message=message)


class FbObject(metaclass=ABCMeta):
    @abstractmethod
    def __dict__(self):
        raise NotImplementedError()

    @staticmethod
    def throw_if_greater_than_limit(value, limit: int, value_name: str):
        if value_name and not isinstance(value_name, str):
            raise TypeError('value_description must be instance of string.')
        length = len(value)
        if length > limit:
            error_message = 'Limit is {limit} - {value_name} length is {length}'.format(limit=limit,
                                                                                        length=length,
                                                                                        value_name=value_name)
            raise ValueError(error_message)


class StructuredPayload(FbObject):
    TEMPLATE_TYPE_GENERIC = 'generic'
    TEMPLATE_TYPE_BUTTON = 'button'

    @abstractmethod
    def __dict__(self):
        raise NotImplementedError()


class Attachment(FbObject):
    _types = ['image', 'audio', 'video', 'file', 'template']
    TYPE_IMAGE = 'image'
    TYPE_AUDIO = 'audio'
    TYPE_VIDEO = 'video'
    TYPE_FILE = 'file'
    TYPE_TEMPLATE = 'template'

    def __init__(self, type: str, payload: StructuredPayload):
        self._type = type
        self._payload = payload

        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'type': self._type,
            'payload': self._payload.__dict__()
        }

    def throw_if_not_valid(self):
        if self._type not in self._types:
            raise ValueError(
                'Invalid type. Given: {given}. Expected: {expected}.'.format(given=self._type,
                                                                             expected=self._types))

        if not isinstance(self._payload, StructuredPayload):
            raise TypeError('Invalid payload type.')


class QuickReply(FbObject):
    CONTENT_TYPE_TEXT = 'text'

    def __init__(self, title: str, payload: str):
        self._content_type = self.CONTENT_TYPE_TEXT
        self._title = title
        self._payload = payload

        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'content_type': self._content_type,
            'title': self._title,
            'payload': self._payload
        }

    def throw_if_not_valid(self):
        title_limit = 1000
        self.throw_if_greater_than_limit(value=self._title, limit=title_limit, value_name='title')
        payload_limit = 20
        self.throw_if_greater_than_limit(value=self._payload, limit=payload_limit, value_name='payload')


class Message(FbObject):
    def __init__(self, text=None, attachment=None, quick_replies=None, metadata=None):
        self._text = text
        self._attachment = attachment
        self._quick_replies = quick_replies
        self._metadata = metadata

        self.throw_if_not_valid()

    def __dict__(self):
        template = dict()
        if self._text:
            template.update({'text': self._text})
        if self._attachment:
            template.update({'attachment': self._attachment})
        if self._quick_replies:
            template.update({'quick_replies': self._quick_replies})
        if self._metadata:
            template.update({'metadata': self._metadata})

        return template

    def throw_if_not_valid(self):
        if self._attachment and self._text:
            raise ValueError('text and attachment are mutually exclusive.')

        if self._attachment:
            if not isinstance(self._attachment, Attachment):
                raise TypeError('Invali attachment type.')

        if self._text:
            text_limit = 320
            self.throw_if_greater_than_limit(value=self._text, limit=text_limit, value_name='text')

        if self._quick_replies:
            if not all(isinstance(quick_reply, QuickReply) for quick_reply in self._quick_replies):
                raise TypeError('Invalid quick reply type.')
            quick_replies_limit = 10
            self.throw_if_greater_than_limit(value=self._quick_replies, limit=quick_replies_limit,
                                             value_name='quick_replies')

        if self._metadata:
            metadata_limit = 1000
            self.throw_if_greater_than_limit(value=self._metadata, limit=metadata_limit, value_name='metadata')


class Button(FbObject):
    _types = ['web_url', 'postback']
    TYPE_POSTBACK = 'postback'
    TYPE_WEB_URL = 'web_url'

    def __init__(self, type: str, title, url=None, payload=None):
        self._type = type
        self._title = title
        self._url = url
        self._payload = payload

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'type': self._type,
            'title': self._title,
        }
        if self._url:
            template.update({'url': self._url})
        if self._payload:
            template.update({'payload': self._payload})

        return template

    def throw_if_not_valid(self):
        if self._type.lower() not in self._types:
            raise ValueError('Invalid type. Given: {given}. Expected: {expected}.'.format(given=self._type,
                                                                                          expected=self._types))

        title_limit = 20
        self.throw_if_greater_than_limit(value=self._title, limit=title_limit, value_name='title')

        if self._type.lower() == self.TYPE_WEB_URL:
            if self._payload:
                raise ValueError('If type is web_url, payload must be None.')
            if not self._url:
                raise ValueError('Url is required.')

        if self._type.lower() == self.TYPE_POSTBACK:
            if self._url:
                raise ValueError('If type is postback, web_url must be None.')
            if not self._payload:
                raise ValueError('Postback is required.')


class Element(FbObject):
    def __init__(self, title: str, item_url=None, image_url=None, subtitle=None, buttons=None):
        self._title = title
        self._item_url = item_url
        self._image_url = image_url
        self._subtitle = subtitle
        self._buttons = buttons

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'title': self._title,
        }
        if self._item_url:
            template.update({'item_url': self._item_url})
        if self._image_url:
            template.update({'image_url': self._image_url})
        if self._subtitle:
            template.update({'subtitle': self._subtitle})
        if self._buttons:
            template.update({'buttons': [button.__dict__() for button in self._buttons]})

        return template

    def throw_if_not_valid(self):
        title_limit = 80
        self.throw_if_greater_than_limit(value=self._title, limit=title_limit, value_name='title')

        if self._subtitle:
            subtitle_limit = 80
            self.throw_if_greater_than_limit(value=self._subtitle, limit=subtitle_limit, value_name='subtitle')

        if self._buttons:
            buttons_limit = 3
            self.throw_if_greater_than_limit(value=self._buttons, limit=buttons_limit, value_name='buttons')

        if not all(isinstance(button, Button) for button in self._buttons):
            raise TypeError('Invalid button type.')


class GenericPayload(StructuredPayload):
    def __init__(self, elements: list):
        self._template_type = self.TEMPLATE_TYPE_GENERIC
        self._elements = elements

        self.throw_if_not_valid()

    def __dict__(self):
        template = {
            'template_type': self._template_type,
        }
        if self._elements:
            template.update({'elements': [element.__dict__() for element in self._elements]})

        return template

    def throw_if_not_valid(self):
        elements_limit = 10
        self.throw_if_greater_than_limit(value=self._elements, limit=elements_limit, value_name='elements')

        if not all(isinstance(element, Element) for element in self._elements):
            raise TypeError('Invalid element type.')


class ButtonPayload(StructuredPayload):
    def __init__(self, text: str, buttons: list):
        self._template_type = self.TEMPLATE_TYPE_BUTTON
        self._text = text
        self._buttons = buttons

        self.throw_if_not_valid()

    def __dict__(self):
        return {
            'text': self._text,
            'template_type': self._template_type,
            'buttons': [button.__dict__() for button in self._buttons]
        }

    def throw_if_not_valid(self):
        text_limit = 320
        self.throw_if_greater_than_limit(value=self._text, limit=text_limit, value_name='text')

        buttons_limit = 3
        self.throw_if_greater_than_limit(value=self._buttons, limit=buttons_limit, value_name='buttons')

        if not all(isinstance(button, Button) for button in self._buttons):
            raise TypeError('Invalid button type.')
