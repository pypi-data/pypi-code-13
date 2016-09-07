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
	self.attributes['markdown'] = val

    @markdown.setter
    def html(self, val):
        self.attributes['markdown'] = val

    @property
    def html(self):
        self.attributes['html'] = val

    @html.setter
    def html(self, val):
        self.attributes['html'] = val

    def json(self):
        return json.dumps(self.attributes)

    @classmethod
    def url(cls):
        return '/messages'

