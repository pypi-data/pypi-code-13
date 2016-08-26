# -*- coding: utf-8 -*-

import json as pjson
from json import JSONEncoder
from datetime import datetime
import time

class JSON(JSONEncoder):

    def default(self, o):
        if hasattr(o, '__json__') and callable(getattr(o, '__json__')):
            return o.__json__()

        if hasattr(o, '__dict__'):
            return o.__dict__

        if isinstance(o, datetime):
            return int(time.mktime(o.timetuple()))

        raise TypeError(repr(o) + " is not JSON serializable")

    @classmethod
    def stringify(cls, o, **kws):
        return pjson.dumps(o, cls=cls, ensure_ascii=False, **kws)

    @classmethod
    def parse(cls, str, **kws):
        return pjson.loads(str, **kws)

    @classmethod
    def dict(cls, o, **kws):
        return cls.parse(cls.stringify(o, **kws))


