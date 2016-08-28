# -*- coding: utf-8 -*-

import pickle
from datetime import datetime

from torsession import SessionBase, SessionManagerBase, gen_session_id


class Session(SessionBase):
    def __getitem__(self, key):
        return self.data.get(key, None)

    def __setitem__(self, key, val):
        self.collection.update(
            {'_session_id': self.id},
            {'$set': {key: pickle.dumps(val)}}
        )
        self.data[key] = val

    def __delitem__(self, key):
        self.collection.update(
            {'_session_id': self.id},
            {'$unset': {key: ''}}
        )

        if key in self.data:
            del self.data[key]

    get = __getitem__
    set = __setitem__
    delete = __delitem__

    def get_all(self):
        return self.data

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


class SessionManager(SessionManagerBase):
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
        session.pop("_id")

        for key, val in session.items():
            session[key] = pickle.loads(val)

        return Session(self.collection, session_id, expired_time, **session)
