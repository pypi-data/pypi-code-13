import logging
import socket
import sys

from werkzeug.contrib.wrappers import DynamicCharsetRequestMixin
from werkzeug.wrappers import Request as BaseRequest, Response
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.routing import Rule
from flask import request as flask_current_request

from lymph.core.interfaces import Interface
from lymph.core.services import ServiceInstance
from lymph.core import trace
from lymph.utils.logging import setup_logger
from lymph.exceptions import SocketNotCreated, NoSharedSockets
from lymph.web.interfaces import Request
from lymph.utils import sockets
from lymph.core.trace import Group
from lymph.web.wsgi_server import LymphWSGIServer
from lymph.web.routing import HandledRule
logger = logging.getLogger(__name__)


def flymph(app):
    class WebServiceInterface(Interface):
        NotFound = NotFound
        MethodNotAllowed = MethodNotAllowed

        def __init__(self, *args, **kwargs):
            super(WebServiceInterface, self).__init__(*args, **kwargs)
            self.application = app
            self.wsgi_server = None
            self.uses_static_port = True
            self.http_socket = None

        def __call__(self, *args, **kwargs):
            # Make the object itself a WSGI app
            return self.application(*args, **kwargs)

        def apply_config(self, config):
            super(WebServiceInterface, self).apply_config(config)
            self.http_port = config.get('port')
            self.pool_size = config.get('wsgi_pool_size')
            self.request_trace_id_header = config.get('tracing.request_header')
            self.response_trace_id_header = config.get('tracing.response_header', 'X-Trace-Id')
            def get_trace_id_from_request():
                if self.request_trace_id_header is not None:
                    trace.set_id(flask_current_request.get(self.request_trace_id_header))
            def set_trace_id_to_response(response):
                response.headers[self.response_trace_id_header] = trace.get_id()
                return response
            self.application.before_request(get_trace_id_from_request)
            self.application.after_request(set_trace_id_to_response)

            if not self.http_port:
                self.uses_static_port = False
                self.http_port = sockets.get_unused_port()

        def get_description(self):
            description = super(WebServiceInterface, self).get_description()
            description['http_port'] = self.http_port
            return description

        def on_start(self):
            super(WebServiceInterface, self).on_start()
            setup_logger('werkzeug')
            setup_logger('gevent')
            if self.uses_static_port:
                try:
                    socket_fd = self.container.get_shared_socket_fd(self.http_port)
                except NoSharedSockets:
                    pass
                except SocketNotCreated:
                    logger.warning("socket for port %s wasn't created by node, binding from instance instead", self.http_port)
                else:
                    self.http_socket = sockets.create_socket('fd://%s' % socket_fd)
            if not self.http_socket:
                address = '%s:%s' % (self.container.server.ip, self.http_port)
                self.http_socket = sockets.create_socket(address)
            self.wsgi_server = LymphWSGIServer(self.http_socket, self.application, spawn=Group(self.pool_size))
            self.wsgi_server.start()

            web_instance = ServiceInstance(
                id=self.id,
                identity=self.container.identity,
                hostname=socket.gethostname(),
                ip=self.container.server.ip,
                http_port=self.http_port,
            )
            self.container.service_registry.register(self.name, web_instance, namespace='http')

        def on_stop(self, **kwargs):
            self.wsgi_server.stop()
            super(WebServiceInterface, self).on_stop()

        def get_wsgi_application(self):
            return self.application

    return WebServiceInterface


