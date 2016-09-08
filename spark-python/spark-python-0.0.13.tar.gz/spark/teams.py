import json


class Team(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['id'] = None
            self.attributes['name'] = None

    @property
    def id(self):
        return self.attributes['id']

    @property
    def name(self):
        return self.attributes['name']

    @name.setter
    def name(self, val):
        self.attributes['name'] = val

    def get_json(self):
        return json.dumps(self.attributes)

    @classmethod
    def from_json(cls, obj):
        instance = cls(attributes=obj)
        return instance

    @classmethod
    def url(self):
        return '/teams'

    @classmethod
    def get(cls, session, name=None):
        """
        Retrieve team list
        :param session: Session object
        :return: list teams available in the current session
        """
        ret = []
        teams = json.loads(session.get(cls.url()).text)['items']
        for team in teams:
            obj = cls.from_json(team)
            if name == obj.name:

                return obj
            else:
                ret.append(obj)
        return ret

    def create(self, session):
        resp = session.post(self.url(), self.get_json())
        obj = self.from_json(resp.json())
        return obj

    def delete(self, session):
        url = self.url() + '/{}'.format(self.id)
        resp = session.delete(url)
        return resp
