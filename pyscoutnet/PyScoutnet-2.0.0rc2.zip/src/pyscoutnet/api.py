# -*- coding: utf-8 -*-

'''
Copyright (c) 2016, Jan Brohl <janbrohl@t-online.de>.
All rights reserved.
See LICENSE.txt
'''
import json
import requests
import collections
import functools

__all__ = ["ScoutnetObject", "ScoutnetCollection", "ScoutnetEvent",
           "ScoutnetGroup", "ScoutnetSection", "ScoutnetUrl", "ScoutnetAPI"]


class ScoutnetObject(object):
    _base_url = "https://www.scoutnet.de/api/0.2/"
    _slots = ()
    _methods = ()

    def __init__(self, object_dict=None):
        if object_dict is None:
            object_dict = {}
        for k in self._slots:
            v = object_dict.get(k, None)
            if k == "id":
                v = int(v)
            setattr(self, k, v)

    def __getattr__(self, name):
        if name in self._methods:
            return functools.partial(self._get, name)
        raise AttributeError(name)

    def _get(self, name, *args):
        params = {"json": json.dumps(args)}
        r = requests.get("%s%s/" % (self.api_url, name), params)
        return r.json(object_hook=_object_hook)

    def _dict(self):
        return dict((k, getattr(self, k, None)) for k in self._slots)

    @property
    def api_url(self):
        return "%s%s" % (self._base_url, self._path())

    def _path(self):
        return "%s/%s/" % (self.kind, self.id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__,  self._dict())


class ScoutnetCollection(ScoutnetObject, collections.Sequence):
    _slots = ("kind", "element_kind", "elements")

    def __init__(self, object_dict):
        if isinstance(object_dict["elements"], dict):
            object_dict["elements"] = sorted(object_dict["elements"].items())
        ScoutnetObject.__init__(self, object_dict)

    def __contains__(self, item):
        return item in self.elements

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def __len__(self):
        return len(self.elements)


class ScoutnetEvent(ScoutnetObject):
    _slots = ('description', 'end_date', 'start_date', 'group_id',
              'id', 'keywords', 'kind', 'last_modified_by',
              'last_modified_on', 'location', 'organizer', 'start_date',
              'start_time', 'target_group', 'target_group', 'title',
              'uid', 'url', 'url_text', 'zip')
    _methods = ('group',)


class ScoutnetGroup(ScoutnetObject):
    _slots = ('city', 'country', 'district', 'federal_state',
              'global_id', 'internal_id', 'kind', 'layer', 'name', 'zip')
    _methods = ('events', 'parent', 'parents',
                'sections', 'urls', 'children')

    @property
    def id(self):
        return int(self.global_id)


class ScoutnetSection(ScoutnetObject):
    _slots = ('color', 'end_age', 'id', 'kind', 'start_age')


class ScoutnetUrl(ScoutnetObject):
    _slots = ('group_id', 'id', 'kind', 'text', 'url')


class ScoutnetAPI(ScoutnetObject):
    _methods = ('event', 'events', 'group', 'groups',
                'section', 'sections', 'url', 'urls')

    def _path(self):
        return ""

_kind2class = {"section": ScoutnetSection, "url": ScoutnetUrl,
               "group": ScoutnetGroup, "event": ScoutnetEvent,
               "collection": ScoutnetCollection}


def _object_hook(obj):
    cls = _kind2class.get(obj.get("kind", None), None)
    if cls:
        return cls(obj)
    else:
        return obj
