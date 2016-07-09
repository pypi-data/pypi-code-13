# -*- coding: utf-8 -*-

import logging
import sys

import gevent
import gevent.pool
import zmq

from disciple.contrib.socket import SocketBase


class BaseWorker(SocketBase):

    def __init__(self, methods=None, context=None, zmq_socket=zmq.PULL):
        super(BaseWorker, self).__init__(zmq_socket, context=context)

        if methods is None:
            methods = self

        self._methods = self._filter_methods(BaseWorker, self, methods)
        self._receiver_task = None

    def close(self):
        self.stop()
        super(BaseWorker, self).close()

    def __call__(self, method, *args):
        if method not in self._methods:
            raise NameError(method)
        return self._methods[method](*args)

    @staticmethod
    def _filter_methods(cls, self, methods):
        if isinstance(methods, dict):
            return methods
        server_methods = set(k for k in dir(cls) if not k.startswith('_'))
        return dict((k, getattr(methods, k))
                    for k in dir(methods)
                    if callable(getattr(methods, k)) and
                    not k.startswith('_') and k not in server_methods
                    )

    def _receiver(self):
        while True:
            event = self._events.recv()
            try:
                if event.name not in self._methods:
                    raise NameError(event.name)
                self._context.hook_load_task_context(event.header)
                self._context.hook_server_before_exec(event)
                self._methods[event.name](*event.args)
                # In Push/Pull their is no reply to send, hence None for the
                # reply_event argument
                self._context.hook_server_after_exec(event, None)
            except Exception:
                exc_infos = sys.exc_info()
                try:
                    logging.exception('')
                    self._context.hook_server_inspect_exception(event, None, exc_infos)
                finally:
                    del exc_infos

    def run(self):
        self._receiver_task = gevent.spawn(self._receiver)
        try:
            self._receiver_task.get()
        finally:
            self._receiver_task = None

    def stop(self):
        if self._receiver_task is not None:
            self._receiver_task.kill(block=False)