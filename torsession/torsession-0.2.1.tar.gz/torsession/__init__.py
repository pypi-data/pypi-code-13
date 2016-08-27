# -*- coding: utf-8 -*-

'''An asynchronous session backend with mongodb for tornado'''

import pickle
import uuid
from datetime import datetime, timedelta

from tornado import gen

VERSION = (0, 2, 1)


def get_version():
    return '.'.join(map(str, VERSION))

__version__ = get_version()


def gen_session_id():
    return str(uuid.uuid1())


class Session(object):
    def __init__(self, collection, id_, expired_time, **data):
        self.collection = collection
        self.id = id_
        self.expired_time = expired_time
        self.data = data

    @gen.coroutine
    def get(self, key):
        """get value mapped to key"""

        assert key not in ["_id", "_session_id", "_expired_time"]

        raise gen.Return(self.data.get(key, None))

    @gen.coroutine
    def set(self, key, value):
        """set key=value pair to the session"""

        assert key not in ["_id", "_session_id", "_expired_time"]

        yield self.collection.update(
            {'_session_id': self.id},
            {'$set': {key: pickle.dumps(value)}}
        )
        self.data[key] = value
        raise gen.Return()

    @gen.coroutine
    def delete(self, key):
        """delete key from the session"""

        yield self.collection.update(
            {'_session_id': self.id},
            {'$unset': {key: ''}}
        )

        if key in self.data:
            del self.data[key]

        raise gen.Return()

    @gen.coroutine
    def clear(self):
        """clear the session"""

        yield self.collection.remove({'_session_id': self.id})
        self.data.clear()

        raise gen.Return()

    @gen.coroutine
    def refresh_id(self):
        """refresh the session id"""

        new_id = gen_session_id()
        yield self.collection.update(
            {'_session_id': self.id},
            {"$set": {"_session_id": new_id}}
        )
        self.id = new_id

        raise gen.Return()


class SessionManager(object):
    EXPIRED_AFTER = timedelta(days=3)

    def __init__(self, collection, expired_after=None):
        self.collection = collection
        self.expired_after = expired_after or self.EXPIRED_AFTER

    @gen.coroutine
    def new_session(self):
        '''New session on server'''

        document = {
            '_session_id': gen_session_id(),
            '_expired_time': datetime.now() + self.expired_after
        }
        yield self.collection.insert(document)

        raise gen.Return(Session(
            self.collection,
            document['_session_id'],
            document['_expired_time']
        ))

    @gen.coroutine
    def load_session(self, session_id):
        session = yield self.collection.find_one({
            '_session_id': session_id
        })

        if not session:
            raise gen.Return()

        session_id = session.pop("_session_id")
        expired_time = session.pop("_expired_time")

        raise gen.Return(Session(
            self.collection, session_id, expired_time, **session
        ))
