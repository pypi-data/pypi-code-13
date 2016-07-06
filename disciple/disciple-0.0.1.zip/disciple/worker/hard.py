# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import uuid
import zmq.green as zmq
import logging
from zmq import error as zmq_error


class HardWorker(object):
    def __init__(self, identity=None, name=None, kazoo_instance=None, timeout=0.250):

        self.ident = identity or str(uuid.uuid4())
        self.name = name or self.__class__.__name__

        self.log = logging.getLogger("%s.%s" % (__name__, self.name))

        self.timeout = timeout

        self._zmq_ctx = zmq.Context()
        self._zmq_socket = self._zmq_ctx.socket(zmq.PULL)

        self._zmq_socket.setsockopt(zmq.IDENTITY,
                                    "%s.%s" % (self.ident, zmq.PULL))

        self.poller = zmq.Poller()

    def connect(self, out_addr):
        _o_b = None, None
        try:
            _o_b = self._zmq_socket.connect(out_addr) or True
            self.poller.register(self._zmq_socket, zmq.POLLIN)
        except zmq_error.ZMQError:
            if _o_b:
                self._zmq_socket.unconnect(out_addr)
            return False
        else:
            return True

    def receive(self):
        socks = dict(self.poller.poll())
        if self._zmq_socket in socks:
            return self._zmq_socket.recv()

