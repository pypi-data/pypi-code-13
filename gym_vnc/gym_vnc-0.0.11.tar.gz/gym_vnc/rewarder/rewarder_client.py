import logging
from gym_vnc import pyprofile
import time
import ujson

from autobahn.twisted import websocket
from twisted.internet import defer

from gym_vnc import error, utils
from gym_vnc.rewarder import env_status, reward_buffer

logger = logging.getLogger(__name__)

class RemoteError(error.Error):
    pass

class RewarderClient(websocket.WebSocketClientProtocol):
    def __init__(self):
        super(RewarderClient, self).__init__()
        self._closed = False
        self._close_message = None

        self._connected = False

    def onConnect(self, request):
        self._request_id = 0
        self._requests = {}

        self.env_status = env_status.EnvStatus()
        self.reward_buffer = reward_buffer.RewardBuffer()

        self.factory.deferred.callback(self)

        self._connected = True

    def send(self, method, body, headers={}, expect_reply=False):
        if self._closed:
            error_message = "Can't send message to closed connection"
            if self._close_message:
                error_message += ": {}".format(self._close_message)
            e = error.Error(error_message)
            if expect_reply:
                d = defer.Deferred()
                d.errback(e)
                return d
            else:
                raise e

        id = self._request_id

        self._request_id += 1
        new_headers = {
            'request_id': id,
            'sent_at': time.time(),
        }
        new_headers.update(headers)

        payload = {
            'method': method,
            'body': body,
            'headers': new_headers,
        }

        logger.debug('Sending message to rewarder: %s', payload)
        self.sendMessage(ujson.dumps(payload), False)

        if expect_reply:
            d = defer.Deferred()
            self._requests[id] = (payload, d)
            return d
        else:
            return None

    def recv(self, context, response):
        method = response['method']
        body = response['body']
        headers = response['headers']

        # Gets called by RewarderClient
        if method == 'env.reward':
            reward = body['reward']
            done = body['done']
            info = body['info']
            logger.debug('Received env.reward: reward=%s done=%s info=%s', reward, done, info)
            self.reward_buffer.push(reward, done, info, remote_time=headers['sent_at'], local_time=context['start'])
        elif method == 'env.observation':
            jsonable = body['observation']
            logger.debug('Received env.observation: observation=%s', jsonable)
            self.reward_buffer.set_observation(jsonable)
        elif method == 'env.describe':
            env_id = body['env_id']
            env_state = body['env_state']
            logger.debug('Received env.describe: env_id=%s env_state=%s', env_id, env_state)
            self.env_status.set_env_info(env_state, env_id=env_id)
        elif method in ['rpc.reply.error', 'rpc.reply.control.ping', 'rpc.reply.env.reset']:
            assert headers.get('parent_request_id') is not None
        elif method == 'connection.close':
            assert headers.get('parent_request_id') is None
            logger.debug('Server hanging up: %s', body['message'])
            self._close_message = body['message']
        else:
            logger.error('Unrecognized websocket method: method=%s body=%s headers=%s (consider adding to rewarder_state.py)', method, body, headers)
            return

        parent_id = headers.get('parent_request_id')
        if parent_id is not None:
            try:
                spec = self._requests.pop(parent_id)
            except KeyError:
                logger.error('Received extra reply to %d; ignoring: method=%s body=%s headers=%s ', parent_id, method, body, headers)
            else:
                request, d = spec
                if method != 'rpc.reply.error':
                    d.callback((context, request, response))
                else:
                    e = RemoteError('[{}] Remote error: {}'.format(self.factory.label, body['message']))
                    d.errback(e)

    def onMessage(self, payload, isBinary):
        logger.debug('Received payload: %s', payload)
        assert not isBinary
        payload = ujson.loads(payload)

        context = {'start': time.time()}
        latency = context['start'] - payload['headers']['sent_at']
        pyprofile.incr('rewarder_protocol.messages')
        pyprofile.incr('rewarder_protocol.messages.{}'.format(payload['method']))

        # Double latency to model RTT
        pyprofile.timing('rewarder_protocol.latency.rtt.skew_unadjusted', 2*latency)
        if latency < 0:
            pyprofile.incr('rewarder_protocol.latency.rtt.skew_unadjusted.negative')

        self.recv(context, payload)

    def onClose(self, wasClean, code, reason):
        if not self._closed:
            error_message = '[{}] Lost connection: {} (clean={} code={})'.format(self.factory.label, reason, wasClean, code)
            if not self._connected:
                error_message += "\n\nHINT: Your rewarder may not have come up yet, or may have crashed. Some Docker setups (such as Docker for Mac) accept TCP connections even if the listener is closed, which may have happened here. Please check the Docker logs for your rewarder process."
            reason = error.Error(error_message)
            # TODO: it's not an error if we requested it
            self.factory.error_buffer.record(reason)
            try:
                self.factory.deferred.errback(utils.format_error(reason))
            except defer.AlreadyCalledError:
                pass
        else:
            error_message = "In-flight message failed due to closed connection"
            if self._close_message:
                error_message += ": {}".format(self._close_message)
            reason = error.Error(error_message)

        for request, d in self._requests.values():
            d.errback(reason)

        self._closed = True

    def close(self):
        self._closed = True
        self.transport.loseConnection()
