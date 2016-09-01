# -*- coding: utf-8 -*-
from epitropos import plugin
from malibu.util.log import LoggingDriver
from restify import routing
from restify.routing.base import (
    api_route,
    json_response
)


@routing.routing_module
class HealthAPIRouter(routing.base.APIRouter):
    """ Router for service health endpoints.

        GET /_health
        GET /_health/auth
        GET /_health/storage
    """

    def __init__(self, manager):

        super(HealthAPIRouter, self).__init__(manager)

        self._log = LoggingDriver.find_logger()

    @api_route(
        path='/_health',
        actions=['GET'],
        returns='application/json'
    )
    @json_response
    def health_get(self):
        """ GET /_health

            Simply returns a static JSON message as a ping response
            from external call.
        """

        resp = self.generate_bare_response()
        resp['status'] = 'okay'

        return resp

    @api_route(
        path='/_health/auth',
        actions=['GET'],
        returns='application/json'
    )
    @json_response
    def auth_backend_health_get(self):
        """ GET /_health/auth

            Attempts to ping the active auth backend to perform
            a health check. Returns the value.
        """

        plug = plugin.authentication()

        if plug.ping():
            resp = self.generate_bare_response()
            resp['status'] = 'okay'
        else:
            resp = self.generate_error_response(code=500)
            resp['status'] = 'down'

        return resp

    @api_route(
        path='/_health/storage',
        actions=['GET'],
        returns='application/json'
    )
    @json_response
    def storage_health_get(self):
        """ GET /_health/storage

            Attempts to ping the storage backend to perform a health
            check. Returns the value.
        """

        plug = plugin.storage()

        if plug.ping():
            resp = self.generate_bare_response()
            resp['status'] = 'okay'
        else:
            resp = self.generate_error_response(code=500)
            resp['status'] = 'down'

        return resp
