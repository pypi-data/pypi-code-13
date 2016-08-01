
import posixpath

import requests





class QDB(object):

    def __init__(self, baseurl, user='admin', password='admin'):
        self.baseurl = baseurl
        self.user = user
        self.password = password

    def _request(self, action, *path, **kwargs):
        url = posixpath.join(self.baseurl, *path)
        return requests.request(action, url, **kwargs)

    def _get(self, *path, **kwargs): return self._request('GET', *path, **kwargs)
    def _getj(self, *path, **kwargs): return self._get(*path, **kwargs).json()
    def _post(self, *path, **kwargs): return self._request('POST', *path, **kwargs)
    def _postj(self, *path, **kwargs): return self._post(*path, **kwargs).json()

    def status(self, gc=False):
        params = {}
        if gc: params['gc'] = 'true'
        return self._getj('status', params=params)

    def queues(self):
        return self._getj('q')

    def qstatus(self, q):
        return self._getj('q', q)

    def qconfig(self, q, **configs):
        """
        valid config keys:
            maxSize - max size of the queue
            maxPayloadSize - max size of each item in the queue
            contentType - HTTP content-type to set on retrieval
            warnAfter - duration before warning about lack of data
            errorAfter - duration before erroring about lack of data
        """
        return self._postj('q', q, data=configs)

    def qappend(self, q, data, routingKey=None):
        params = {}
        if routingKey is not None: params['routingKey'] = routingKey
        return self._postj('q', q, 'messages', params=params, data=data)

    def qmappend(self, q, batchdata):
        """
        Note that batchdata must be formulated as described in the docs
        """
        params={'multiple':'true'}
        return self._postj('q', q, 'messages', params=params, data=batchdata)

    def qgetone(self, q, from_id=None, from_time=None, **extra):
        if (from_id, from_time) == (None, None):
            raise ValueError("Must specify one of from_id or from_time")
        params={'single': 'true' }
        params.update(extra)
        if from_id is not None: params['fromId'] = str(from_id)
        if from_time is not None: params['from'] = from_time
        return self._get('q', q, 'messages', params=params)

    def qgetstream(self, q, **params):
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
        stream = self._get('q', q, 'messages', params=params, stream=True).iter_lines()
        for r in stream:
            yield r

    def qtimeline(self, q, **extra):
        return self._getj('q', q, 'timeline', params=extra)

    def users(self):
        return self._getj('users')

    def mkuser(self, user, password, admin=False):
        d = { 'password': password }
        if admin: { 'admin': 'true' }
        return self._postj('users', user, data=d)

    def dbs(self):
        return self._getj('db')

    def chpass(self, newpass):
        result = self._postj('users', self.user, data={'password':newpass})
        self.password = newpass
        return result


