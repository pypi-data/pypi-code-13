
import posixpath

import requests



class Server(object):
    """
    Connection wrapper object
    """

    def __init__(self, baseurl, user='admin', password='admin'):
        self.baseurl = baseurl
        self.user = user
        self.password = password
        self._session = requests.Session()

    def _request(self, action, *path, **kwargs):
        """
        All requests go through here so they use common auth
        """
        url = posixpath.join(self.baseurl, *path)
        if not 'auth' in kwargs:
            kwargs['auth'] = (self.user, self.password)
        return self._session.request(action, url, **kwargs)

    # convenience functions
    def _get(self, *path, **kwargs): return self._request('GET', *path, **kwargs)
    def _getj(self, *path, **kwargs): return self._get(*path, **kwargs).json()
    def _post(self, *path, **kwargs): return self._request('POST', *path, **kwargs)
    def _postj(self, *path, **kwargs): return self._post(*path, **kwargs).json()

    # server level

    def status(self, gc=False):
        """
        Retrieve server status
        """
        params = {}
        if gc: params['gc'] = 'true'
        return self._getj('status', params=params)

    def users(self):
        """
        Retrieve the defined users
        """
        return self._getj('users')

    def mkuser(self, user, password, admin=False):
        """
        Create a user/password combination.
        Set admin=True to give them admin privileges.
        """
        d = { 'password': password }
        if admin: { 'admin': 'true' }
        return self._postj('users', user, data=d)

    def chpass(self, newpass):
        """
        Change the current user's password
        """
        result = self._postj('users', self.user, data={'password':newpass})
        self.password = newpass
        return result

    def dbs(self):
        """
        Get the raw list of databases
        """
        return self._getj('db')

    def mkdb(self, name):
        return self._postj('db', name)

    def Database(self, dbname='default'):
        """
        Get the Database object for the database of the specified name (aka id).
        Note that this doesn't mean it *exists*, it just provides a handle to it.
        """
        return Database(self, dbname)

    def Databases(self):
        for d in self.dbs():
            yield Database(self, d['id'])

    def Queue(self, dbname, q):
        return Database(self, dbname).Queue(self, q)


class Database(object):
    """
    A set of QDB.io queues
    """
    def __init__(self, server, dbname):
        self.srv = server
        self.dbid = dbname

    def _get(self, *path, **kwargs): return self.srv._request('GET', 'db', self.dbid, *path, **kwargs)
    def _post(self, *path, **kwargs): return self.srv._request('POST', 'db', self.dbid, *path, **kwargs)
    def _getj(self, *path, **kwargs): return self._get(*path, **kwargs).json()
    def _postj(self, *path, **kwargs): return self._post(*path, **kwargs).json()

    def queues(self):
        return self._getj('q')

    def Queue(self, q):
        return Queue(self, q)

    def Queues(self):
        for q in self.queues():
            yield Queue(self, q['id'])


class Queue(object):
    """
    A QDB.io queue
    """
    def __init__(self, qdb, name):
        self.qdb = qdb
        self.qid = name

    def _get(self, *path, **kwargs): return self.qdb._get('q', self.qid, *path, **kwargs)
    def _post(self, *path, **kwargs): return self.qdb._post('q', self.qid, *path, **kwargs)
    def _getj(self, *path, **kwargs): return self._get(*path, **kwargs).json()
    def _postj(self, *path, **kwargs): return self._post(*path, **kwargs).json()

    def status(self):
        return self._getj()

    def config(self, **configs):
        """
        (re)configure the specified queue

        valid config keys:
            maxSize - max size of the queue
            maxPayloadSize - max size of each item in the queue
            contentType - HTTP content-type to set on retrieval
            warnAfter - duration before warning about lack of data
            errorAfter - duration before erroring about lack of data
        """
        return self._postj(data=configs)

    def append(self, data, routingKey=None):
        params = {}
        if routingKey is not None: params['routingKey'] = routingKey
        return self._postj('messages', params=params, data=data)

    def mappend(self, batchdata):
        """
        Note that batchdata must be formulated as described in the docs
        """
        params={'multiple':'true'}
        return self._postj('messages', params=params, data=batchdata)

    def getone(self, from_id=None, from_time=None, **extra):
        if (from_id, from_time) == (None, None):
            raise ValueError("Must specify one of from_id or from_time")
        params={'single': 'true' }
        params.update(extra)
        if from_id is not None: params['fromId'] = str(from_id)
        if from_time is not None: params['from'] = from_time
        return self._get('messages', params=params)

    def getstream(self, **params):
        """
        Supported params:
            from - messages from this time
            to - messages before this time
            fromId - messages starting with this Id
            toId - messages before this Id
            limit - stop after this many messages
            noHeaders - don't send the header json
            noPayload - don't send the message payloads
            noLengthPrefix - don't prefix the header JSON with its length
            timeoutMs -
            keepaliveMs -
            keepAlive -
            separator -
            ###
            grep - find messages matching the supplied expression
            routingKey - find messages with a routingKey matching the supplied expression
                         (/expr/ is a Java regex ; expr alone is a RabbitMQ expression)
            Note: grep and routingKey are ANDed if both supplied
        return an iterator over a stream of the requested messages.
        Messages are preceded by a header line which is a json netstring
        with its size prepended. Messages themselves are also netstrings
        with their size prepended.
        """
        # TODO: do better, returning a tuple of the  json header json.loads()'d and
        #       the message ; beware newlines in the message
        stream = self._get('messages', params=params, stream=True).iter_lines()
        for r in stream:
            yield r

    def qtimeline(self, bucket_id=None):
        path = [ 'timeline' ]
        if bucket_id is not None:
            path.append(bucket_id)
        return self._getj(*path)




