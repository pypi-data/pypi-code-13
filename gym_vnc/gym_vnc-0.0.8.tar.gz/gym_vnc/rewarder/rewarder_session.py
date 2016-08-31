from autobahn.twisted import websocket
import logging
import time

from twisted.python import failure
from twisted.internet import defer, endpoints

from gym_vnc import error, utils
from gym_vnc.twisty import reactor
from gym_vnc.rewarder import connection_timer, reward_buffer, rewarder_client

logger = logging.getLogger(__name__)

class RewarderSession(object):
    def __init__(self, remotes, error_buffer):
        self.remotes = remotes
        self.reward_buffers = [reward_buffer.RewardBuffer() for _ in remotes]
        self.error_buffer = error_buffer
        self.connect()

        self._requests = {}

    def connect(self):
        utils.blockingCallFromThread(self._connect)

    # Call only from Twisted thread

    def _connect(self):
        deferreds = []

        for i, remote in enumerate(self.remotes):
            d = defer.Deferred()
            deferreds.append(d)

            endpoint = endpoints.clientFromString(reactor, 'tcp:'+remote)
            factory = websocket.WebSocketClientFactory('ws://'+remote)
            factory.protocol = rewarder_client.RewarderClient

            factory.deferred = d
            factory.error_buffer = self.error_buffer
            factory.label = 'rewarder:{}:{}'.format(i, remote)
            factory.rewarder_session = self
            factory.remote = remote
            factory.endpoint = endpoint

            def success(i):
                logger.info('[%s] Rewarder connection established', factory.label)

            def fail(reason):
                reason = error.Error('[{}] Connection failed: {}'.format(factory.label, reason.value))

                try:
                    d.errback(utils.format_error(reason))
                except defer.AlreadyCalledError:
                    raise
            endpoint.connect(factory).addCallback(success).addErrback(fail)

        d = defer.DeferredList(deferreds, fireOnOneErrback=True, consumeErrors=True)

        def success(results):
            # Store the _clients list when connected
            self._clients = [client for success, client in results]
        d.addCallback(success)
        return d

    def reset(self, env_id, seed=0, fps=60, **kwargs):
        # [(True, (context, request, response))]
        result = utils.blockingCallFromThread(
            self._reset,
            env_id=env_id,
            seed=seed,
            fps=fps,
            **kwargs)
        unwrapped = [res for _, res in result]
        # Clear any pending rewards
        self.pop()

        return unwrapped

    def _reset(self, **kwargs):
        deferreds = []

        for client in self._clients:
            d = client.send('rpc.env.reset', kwargs, expect_reply=True)
            deferreds.append(d)

        d = defer.DeferredList(deferreds, fireOnOneErrback=True, consumeErrors=True)
        return d

    def pop(self):
        reward_n = []
        done_n = []
        info_n = []

        for client in self._clients:
            reward, done, info = client.reward_buffer.pop()
            reward_n.append(reward)
            done_n.append(done)
            info_n.append(info)

        return reward_n, done_n, info_n

    def wait(self, timeout=None):
        deadline = time.time() + timeout
        for client in self._clients:
            if timeout is not None:
                remaining_timeout = deadline - time.time()
            else:
                remaining_timeout = None
            client.reward_buffer.wait_for_step(timeout=remaining_timeout)

    def ping(self):
        result = utils.blockingCallFromThread(self._ping)
        unwrapped = [res for _, res in result]
        return unwrapped

    def _ping(self):
        deferreds = []

        for client in self._clients:
            d = client.send('rpc.control.ping', {}, expect_reply=True)
            deferreds.append(d)

        d = defer.DeferredList(deferreds, fireOnOneErrback=True, consumeErrors=True)
        return d

    def rewards_remote_time(self):
        # TODO: any reason to lock these?
        return [client.reward_buffer.remote_time for client in self._clients]

    def rewards_count(self):
        # TODO: any reason to lock these?
        return [client.reward_buffer.count for client in self._clients]

    def pop_observation(self):
        return [client.reward_buffer.pop_observation() for client in self._clients]

    def connection_time(self):
        result = utils.blockingCallFromThread(self._connection_time)
        unwrapped = [res for _, res in result]
        return unwrapped

    def _connection_time(self):
        deferreds = []
        for client in self._clients:
            endpoint = client.factory.endpoint
            d = connection_timer.start(endpoint)
            deferreds.append(d)

        d = defer.DeferredList(deferreds, fireOnOneErrback=True, consumeErrors=True)
        return d
