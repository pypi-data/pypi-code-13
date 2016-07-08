'''
Created on 23.07.2012

@author: Jan Brohl <janbrohl@t-online.de>
@license: Simplified BSD License - see license.txt
@copyright: Copyright (c) 2012-2016, Jan Brohl <janbrohl@t-online.de>. All rights reserved.
'''
import json
import requests


class ScoutnetObject(object):
    _base_url = "https://www.scoutnet.de/api/0.2/"
    _slots = tuple()
    _methods = tuple()

    def __init__(self, object_dict=None):
        if object_dict:
            for k, v in object_dict.items():
                if k in self._slots:
                    if k == "id":
                        v = int(v)
                    setattr(self, k, v)

    def __getattr__(self, name):
        if name in self._methods:
            return lambda *args: requests.get(self.url() + name + "/", {"json": json.dumps(args)}).json(object_hook=object_hook)
        else:
            raise AttributeError(name)

    def object_dict(self):
        return dict((k, getattr(self, k, None)) for k in self._slots)

    def url(self):
        return self._base_url + self.path()

    def path(self):
        return "%s/%s/" % (self.kind, self.id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.object_dict())

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.object_dict())


class ScoutnetCollection(ScoutnetObject):
    _slots = ("kind", "element_kind", "elements")

    def __init__(self, object_dict):
        if isinstance(object_dict["elements"], dict):
            object_dict["elements"] = object_dict["elements"].items()
        ScoutnetObject.__init__(self, object_dict)

    def __getitem__(self, key):
        return self.elements[key]

    def object_dict(self):
        d = ScoutnetObject.object_dict(self)
        d["elements"] = tuple(self)
        return d


class ScoutnetEvent(ScoutnetObject):
    _slots = ('description', 'end_date', 'start_date', 'group_id', 'id', 'keywords', 'kind', 'last_modified_by', 'last_modified_on',
              'location', 'organizer', 'start_date', 'start_time', 'target_group', 'target_group', 'title', 'uid', 'url', 'url_text', 'zip')
    _methods = tuple("""
    group
    """.split())


class ScoutnetGroup(ScoutnetObject):
    _slots = ('city', 'country', 'district', 'federal_state',
              'global_id', 'internal_id', 'kind', 'layer', 'name', 'zip')
    _methods = ('events', 'parent', 'parents', 'sections', 'urls', 'children')

    @property
    def id(self):
        return self.global_id


class ScoutnetSection(ScoutnetObject):
    _slots = tuple("""
    color end_age id kind start_age
    """.split())


class ScoutnetUrl(ScoutnetObject):
    _slots = tuple("""
    group_id id kind text url
    """.split())


class ScoutnetAPI(ScoutnetObject):
    _methods = tuple("""
    event events group groups section sections url urls
    """.split())

    def path(self):
        return ""


def object_hook(obj):
    kind2class = dict(section=ScoutnetSection, url=ScoutnetUrl,
                      group=ScoutnetGroup, event=ScoutnetEvent,
                      collection=ScoutnetCollection)
    cls = kind2class.get(obj.get("kind", None), None)
    if cls:
        return cls(obj)
    else:
        return obj


def API():
    return ScoutnetAPI()
