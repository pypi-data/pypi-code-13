# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import uuid
import zmq.green as zmq
import logging
import time
from zmq import error as zmq_error


class BalanceDealer(object):

    def __init__(self, identity=None, name=None, kazoo_instance=None, timeout=5):

        self.timeout = timeout
        self.ident = identity or str(uuid.uuid4())
        self.name = name or self.__class__.__name__

        if kazoo_instance:
            kazoo_instance.regiest()

        self.log = logging.getLogger("%s.%s" % (__name__, self.name))

        self._zmq_ctx = zmq.Context()
        self._zmq_socket = self._zmq_ctx.socket(zmq.PUSH)
        self._zmq_socket.setsockopt(zmq.IDENTITY,
                                    "%s.%s" % (self.ident, zmq.PUSH))

    def bind(self, out_addr):
        _o_b = None
        try:
            _o_b = self._zmq_socket.bind(out_addr) or True
        except zmq_error.ZMQError:
            if _o_b:
                self._zmq_socket.unbind(out_addr)
            return False
        else:
            return True

    def distribute(self, msg):

        t1 = time.time()
        while True:
            try:
                if time.time() - t1 > self.timeout:
                    self._raise_warning(msg)
                    break
                self._zmq_socket.send(msg, zmq.NOBLOCK)
            except zmq_error.Again as e:
                pass
            else:
                break

        # def _send():
        #     self._zmq_socket.send(msg)
        #     gevent.sleep(0)
        # gevent.spawn(_send).join()

    def _raise_warning(self, msg):
        print("timeout to send msg {}".format(msg))
