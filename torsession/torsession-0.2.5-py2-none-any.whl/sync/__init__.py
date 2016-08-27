# -*- coding: utf-8 -*-

'''An asynchronous session backend with mongodb for tornado'''

import pickle
from datetime import datetime, timedelta

from torsession import gen_session_id


class Session(object):
    def __init__(self, collection, id_, expired_time, **data):
        self.collection = collection
        self.id = id_
        self.expired_time = expired_time
        self.data = data

    def get(self, key):
        """get value mapped to key"""

        assert key not in ["_id", "_session_id", "_expired_time"]

        return self.data.get(key, None)

    def set(self, key, value):
        """set key=value pair to the session"""

        assert key not in ["_id", "_session_id", "_expired_time"]

        self.collection.update(
            {'_session_id': self.id},
            {'$set': {key: pickle.dumps(value)}}
        )
        self.data[key] = value

    def delete(self, key):
        """delete key from the session"""

        self.collection.update(
            {'_session_id': self.id},
            {'$unset': {key: ''}}
        )

        if key in self.data:
            del self.data[key]

    def clear(self):
        """clear the session"""

        self.collection.remove({'_session_id': self.id})
        self.data.clear()

    def refresh_id(self):
        """refresh the session id"""

        new_id = gen_session_id()
        self.collection.update(
            {'_session_id': self.id},
            {"$set": {"_session_id": new_id}}
        )
        self.id = new_id


class SessionManager(object):
    EXPIRED_AFTER = timedelta(days=3)

    def __init__(self, collection, expired_after=None):
        self.collection = collection
        self.expired_after = expired_after or self.EXPIRED_AFTER

    def new_session(self):
        '''New session on server'''

        document = {
            '_session_id': gen_session_id(),
            '_expired_time': datetime.now() + self.expired_after
        }
        self.collection.insert(document)

        return Session(
            self.collection,
            document['_session_id'],
            document['_expired_time']
        )

    def load_session(self, session_id):
        session = self.collection.find_one({
            '_session_id': session_id
        })

        if not session:
            return

        session_id = session.pop("_session_id")
        expired_time = session.pop("_expired_time")

        return Session(self.collection, session_id, expired_time, **session)
