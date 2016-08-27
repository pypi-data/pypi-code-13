# -*- coding: utf-8 -*-

'''An async && sync session backend with mongodb for tornado'''

import uuid
from datetime import datetime, timedelta

VERSION = (0, 2, 7)


def get_version():
    return '.'.join(map(str, VERSION))

__version__ = get_version()


def gen_session_id():
    return str(uuid.uuid1())


class SessionBase(object):
    def __init__(self, collection, id_, expired_time, **data):
        self.collection = collection
        self.id = id_
        self.expired_time = expired_time
        self.data = data

    def expired(self):
        return self.expired_time < datetime.now()


class SessionManagerBase(object):
    EXPIRED_AFTER = timedelta(days=3)

    def __init__(self, collection, expired_after=None):
        self.collection = collection
        self.expired_after = expired_after or self.EXPIRED_AFTER
