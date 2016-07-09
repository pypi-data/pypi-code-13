# -*- coding: utf-8 -*-

import zmq

from disciple.contrib.socket import SocketBase


class BaseDealer(SocketBase):

    def __init__(self, context=None, zmq_socket=zmq.PUSH):
        super(BaseDealer, self).__init__(zmq_socket, context=context)

    def __call__(self, method, *args):
        self._events.emit(method, args,
                          self._context.hook_get_task_context(), timeout=1)

    def __getattr__(self, method):
        return lambda *args: self(method, *args)




