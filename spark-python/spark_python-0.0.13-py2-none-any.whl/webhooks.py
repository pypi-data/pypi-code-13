import json


class Webhook(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['id'] = None
            self.attributes['event'] = None
            self.attributes['filter'] = None
            self.attributes['resource'] = None
            self.attributes['name'] = None
            self.attributes['targetUrl'] = None

    @property
    def id(self):
        return self.attributes['id']

    @property
    def event(self):
        return self.attributes['event']

    @event.setter
    def event(self, val):
        self.attributes['event'] = val

    @property
    def filter(self):
        return self.attributes['filter']

    @filter.setter
    def filter(self, val):
        self.attributes['filter'] = val

    @property
    def resource(self):
        return self.attributes['resource']

    @resource.setter
    def resource(self, val):
        self.attributes['resource'] = val

    @property
    def name(self):
        return self.attributes['name']

    @name.setter
    def name(self, name):
        self.attributes['name'] = name

    @property
    def targetUrl(self):
        return self.attributes['targetUrl']

    @targetUrl.setter
    def targetUrl(self, val):
        self.attributes['targetUrl'] = val


    def get_json(self):
        return json.dumps(self.attributes)

    @classmethod
    def from_json(cls, obj):
        instance = cls(attributes=obj)
        return instance

    @classmethod
    def url(self):
        return '/webhooks'

    @classmethod
    def get(cls, session):
        items = session.get(cls.url()).json()['items']
        ret = []
        for i in items:
            obj = cls.from_json(i)
            ret.append(obj)
        return ret

    def create(self, session):
        resp = session.post(Webhook.url(), self.get_json())
        obj = Webhook.from_json(resp.json())
        return obj

    def delete(self, session):
        url = self.url() + '/{}'.format(self.id)
        resp = session.delete(url)
        return resp
