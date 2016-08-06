# -*- coding: utf-8 -*-
"""
    pip_services_runtime.clients.RestClient
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract implementation for REST client components
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import requests

from ..State import State
from ..portability.DynamicMap import DynamicMap
from ..data.IdGenerator import IdGenerator
from ..errors.MicroserviceError import MicroserviceError
from ..errors.CallError import CallError
from ..errors.UnknownError import UnknownError
from .AbstractClient import AbstractClient

class RestClient(AbstractClient):

    _default_config = DynamicMap.from_tuples(
        'endpoint.protocol', 'http',
        #'endpoint.host', 'localhost',
        #'endpoint.port', 3000,
        'options.timeout', 60000
    )

    _client = None
    _uri = None
    _timeout = None

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice client component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(RestClient, self).__init__(descriptor)

    def configure(self, config):
        """
        Sets component configuration parameters and switches component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will cause an exception.

        Args:
            config: the component configuration parameters.

        Returns: None

        Raises:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)

        config = config.with_defaults(self._default_config);
        endpoint = config.get_endpoint()
        options = config.get_options()

        # Check for type
        protocol = endpoint.get_protocol()
        if protocol != 'http':
            raise ConfigError(self, 'UnsupportedProtocol', 'Protocol type is not supported by REST transport') \
                .with_details(protocol)

        # Check for host
        if endpoint.get_host() == None:
            raise ConfigError(self, 'NoHost', 'No host is configured in REST transport')

        # Check for port
        if endpoint.get_port() == None:
            raise ConfigError(self, 'NoPort', 'No port is configured in REST transport')

        super(RestClient, self).configure(config)

        self._uri = endpoint.get_uri()
        self._timeout = options.get_nullable_float('timeout') / 1000

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking or reopening after closure.

        Returns: None
        """
        self.check_new_state_allowed(State.Opened)

        self._client = requests

        super(RestClient, self).open()

    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.

        Returns: None  
        """
        self.check_new_state_allowed(State.Closed)

        self._client = None

        super(RestClient, self).close()

    def add_correlation_id(self, params, correlation_id):
        # Automatically generate short ids for now
        if correlation_id == None:
            correlation_id = IdGenerator.short()

        params = params or {}
        params['correlation_id'] = correlation_id
        return params

    def add_filter_params(self, params, filter):
        params = params or {}

        if filter != None:
            for key, value in filter.items():
                params[key] = value

        return params

    def add_paging_params(self, params, paging):
        params = params or {}

        if paging != None:
            if paging['total'] != None:
                params['total'] = paging['total']
            if paging['skip'] != None:
                params['skip'] = paging['skip']
            if paging['take'] != None:
                params['take'] = paging['take']

        return params

    def call(self, method, route, correlation_id = None, params = None, data = None):
        self.check_current_state(State.Opened)

        method = method.upper()
                
        params = params or {}
        params = self.add_correlation_id(params, correlation_id)

        route = self._uri + route
        response = None
        result = None
                    
        try:
            # Call the service
            response = requests.request(method, route, params=params, json=data, timeout=self._timeout)
        except Exception as e:
            error = UnknownError(self, 'UnknownError', 'REST operation failed: ' + str(e)).wrap(e)
            raise error

        if response.status_code == 404 or response.status_code == 204:
            return None

        try:
            # Retrieve JSON data
            result = response.json()
        except:
            # Data is not in JSON
            if response.status_code < 400:
                raise UnknownError(self, 'WrongJson', 'Failed to deserialize JSON data: ' + response.text) \
                    .with_details(response.text)
            else:
                raise UnknownError(self, 'UnknownError', 'Unknown error occured: ' + response.text) \
                    .with_details(response.text)

        # Return result
        if response.status_code < 400:
            return result

        # Raise error
        error = MicroserviceError.from_value(result)
        error.with_status(response.status_code)

        raise error
