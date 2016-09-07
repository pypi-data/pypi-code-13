import json


class Message(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['text'] = None
            self.attributes['roomId'] = None
            self.attributes['markdown'] = None
            self.attributes['html'] = None

    @property
    def text(self):
        return self.attributes['text']

    @text.setter
    def text(self, val):
        self.attributes['text'] = val

    @property
    def roomId(self):
        return self.attributes['roomId']

    @roomId.setter
    def roomId(self, val):
        self.attributes['roomId'] = val

    @property
    def markdown(self):
        return self.attributes['markdown']

    @markdown.setter
    def markdown(self, val):
        self.attributes['markdown'] = val

    @property
    def html(self):
        return self.attributes['html']

    @html.setter
    def html(self, val):
        self.attributes['html'] = val

    def json(self):
        return json.dumps(self.attributes)

    @classmethod
    def url(cls):
        return '/messages'

    @classmethod
    def from_json(cls, obj):
        if isinstance(obj, dict):
            obj = cls(attributes=obj)
        elif isinstance(obj, (str, unicode)):
            obj = cls(attributes=json.loads(obj))
        else:
            raise TypeError('Data must be str or dict')
        return obj

    @classmethod
    def get(cls, session, msgid=None):
        url = '/messages/{}'.format(msgid)
        resp = session.get(url)

        obj = cls.from_json(resp.json())
        return obj

