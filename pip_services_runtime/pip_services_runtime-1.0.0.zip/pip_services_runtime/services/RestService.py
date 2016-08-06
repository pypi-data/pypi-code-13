# -*- coding: utf-8 -*-
"""
    pip_services_runtime.services.RestService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    REST service implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import bottle
import json
import time

from threading import Thread

from ..State import State
from ..portability.DynamicMap import DynamicMap
from ..errors.UnknownError import UnknownError
from ..errors.CallError import CallError
from ..errors.ConnectionError import ConnectionError
from ..data.FilterParams import FilterParams
from ..data.PagingParams import PagingParams
from .AbstractService import AbstractService
from .SimpleServer import SimpleServer

class RestService(AbstractService):
    """
    Interoperable REST service that exposes a specific version of 
    a microservice API via HTTP/HTTPS endpoint to consumers.  
    
    This implementation uses restify library to define RESTful API.
    Authors of specific REST services must register in descendant classes 
    API routes using *registerRoute* in overriden *link* or *register* methods.
    """

    _default_config = DynamicMap.from_tuples( \
        "endpoint.protocol", "http",
        "endpoint.host", "0.0.0.0",
        #"endpoint.port", 3000,
        "options.request_max_size", 1024 * 1024,
        "options.connect_timeout", 60000,
        "options.debug", False
    )

    _service = None
    _server = None
    _debug = False

    def __init__(self, descriptor):
        """
        Creates instance of abstract REST service.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(RestService, self).__init__(descriptor)
        
    def configure(self, config):
        """
        Sets component configuration parameters and switches from component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will cause an exception.
        
        Args:
            config: the component configuration parameters.

        Returns: None

        Args:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)
        
        config = config.with_defaults(self._default_config)
        endpoint = config.get_endpoint()
        
        if endpoint == None:
            raise ConfigError(self, "NoEndpoint", "Endpoint is not configured")

        protocol = endpoint.get_protocol()
        if protocol != 'http':
            raise ConfigError(self, "UnsupportedProtocol", protocol + " protocol is not supported by REST transport") \
                .with_details(protocol)

        if endpoint.get_port() == None:
            raise ConfigError(self, "NoPort", "No port is configured in REST transport")

        super(RestService, self).configure(config)

        options = config.get_options()
        self._debug = options.get_boolean("debug")

    def link(self, components):
        """
        Sets references to other microservice components to enable their 
        collaboration. It is recommended to locate necessary components
        and cache their references to void performance hit during normal operations.

        Linking can only be performed once after configuration 
        and will cause an exception when it is called second time or out of order. 

        Args:
            components: references to microservice components.

        Returns: None

        Raises:
            MicroserviceError: when requires components are not found.
        """
        self.check_new_state_allowed(State.Linked)

        # Create instance of bottle application
        self._service = bottle.Bottle(catchall=True, autojson=True)
        
        # Enable CORS requests
        self._service.add_hook('after_request', self._enable_cors)
        self._service.route('/', 'OPTIONS', self._options_handler)
        self._service.route('/<path:path>', 'OPTIONS', self._options_handler)

        # Register (add) flask routes
        self.register()
        
        super(RestService, self).link(components)

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking or reopening after closure.  

        Returns: None

        Raises:
            MicroserviceError: when initialization or connections fail.
        """
        self.check_new_state_allowed(State.Opened)
        
        endpoint = self._config.get_endpoint()
        host = endpoint.get_host()
        port = endpoint.get_port()

        def start_server():
            self._service.run(server=self._server, debug=self._debug)

        # Starting service
        try:
            self._server = SimpleServer(host=host, port=port)

            # Start server in thread
            Thread(target=start_server).start()

            # Give 2 sec for initialization
            #time.sleep(2)
        except Exception as e:
            raise ConnectionError(self, 'OpenFailed', 'REST service opening failed: ' + str(e)).wrap(e)

        super(RestService, self).open()

    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.
        
        Returns: None
        
        Raises:
            MicroserviceError: with closure fails.
        """
        self.check_new_state_allowed(State.Closed)

        try:
            if self._server != None:
                self._server.shutdown()

            self._server = None
        except Exception as e:
            raise ConnectionError(self, 'CloseFailed', 'REST service closing failed: ' + str(e)).wrap(e)
        
        super(RestService, self).close()

    def _enable_cors(self):
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        bottle.response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

    def _options_handler(self, ath = None):
        return

    def send_result(self, result):
        bottle.response.headers['Content-Type'] = 'application/json'
        if result == None: 
            bottle.response.status = 404
            return
        else:
            bottle.response.status = 200
            return json.dumps(result)

    def send_created_result(self, result):
        bottle.response.headers['Content-Type'] = 'application/json'
        if result == None: 
            bottle.response.status = 404
            return
        else:
            bottle.response.status = 201
            return json.dumps(result)

    def send_deleted_result(self):
        bottle.response.headers['Content-Type'] = 'application/json'
        bottle.response.status = 204
        return

    def send_error(self, error):
        bottle.response.headers['Content-Type'] = 'application/json'
        error = CallError(self, 'ExecFailed', 'Execution of REST operation failed: ' + str(error)).wrap(error)
        if error.correlation_id == None:
            error.with_correlation_id(self.get_correlation_id())
        bottle.response.status = error.status
        return json.dumps(error.to_json())

    def get_param(self, param, default = None):
        return bottle.request.params.get(param, default)

    def get_correlation_id(self):
        return bottle.request.query.get('correlation_id')

    def get_filter_params(self):
        data = dict(bottle.request.query.decode())
        data.pop('correlation_id', None)
        data.pop('skip', None)
        data.pop('take', None)
        data.pop('total', None)        
        return FilterParams(data)

    def get_paging_params(self):
        skip = bottle.request.query.get('skip')
        take = bottle.request.query.get('take')
        total = bottle.request.query.get('total')
        return PagingParams(skip, take, total)

    def get_data(self):
        return bottle.request.json

    def register_route(self, method, route, handler):
        method = method.upper()

        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception as e:
                return self.send_error(e)

        self._service.route(route, method, wrapper)

    def register(self):
        pass