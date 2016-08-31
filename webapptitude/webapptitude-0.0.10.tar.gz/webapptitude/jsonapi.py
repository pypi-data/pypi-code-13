"""JSON API contracts and utilities."""

from google.appengine.ext import ndb
from google.appengine.datastore import datastore_query
from google.appengine.api import datastore_errors
from webapp2 import exc as exceptions
from jsonkit import json_encode, json_decode
from gql import query as gql_query_request
from util import RE_NUMERIC_INT, RE_NUMERIC_FLOAT

import webapp2
import re
import logging


def isregex(val):
    return (type(val) is type(RE_NUMERIC_INT))


class ParameterNotFound(exceptions.HTTPBadRequest, BaseException):
    """Exception, for when parameters are missing"""

    detail = 'A required parameter was not present on the request. (%s)'

    def __init__(self, param_name):
        detail = self.detail % param_name
        super(ParameterNotFound, self).__init__(detail=detail)


class ParameterMismatch(ParameterNotFound):
    """Exception, for when parameters are malformed."""

    detail = 'A required parameter did not match its expected format. (%s)'


class JSONRequestHandler(webapp2.RequestHandler):
    """RequestHandler abstraction to enforce API contracts."""

    def __init__(self, *args, **kwargs):
        """Prepare the basic JSON interface parameters."""
        super(JSONRequestHandler, self).__init__(*args, **kwargs)
        self.content_type = 'application/json'

    def dispatch(self):
        """Some light-weight constraints to enforce JSON handling."""
        if not (self.request.content_type == 'application/json'):
            if (self.request.method in ('PUT', 'POST')):
                raise exceptions.HTTPUnprocessableEntity
        self.response.content_type = 'application/json'
        return super(JSONRequestHandler, self).dispatch()

    def fetch_param(self, name, validate=None, optional=False, default=None):
        """Extract a value from query or request body, with validation."""
        value = self.request.input
        for k in name.split('.'):
            value = value.get(k, None)
            if value is None:
                break

        if value is None and (not optional):
            raise ParameterNotFound(name)
        elif value is None:
            return default

        if validate in (int, 'int'):
            if not RE_NUMERIC_INT.match(value):
                raise ParameterMismatch(name)
        if validate in (float, 'float'):
            if not RE_NUMERIC_FLOAT.match(value):
                raise ParameterMismatch(name)
        if validate in (dict, 'dict'):
            if not isinstance(value, dict):
                raise ParameterMismatch(name)

        if isinstance(validate, basestring):
            validate = re.compile(validate)

        if isregex(validate):
            if not validate.match(value):
                raise ParameterMismatch(name)

        return value


def assert_authorization(handler, model=None, instance=None):
    """Simple wrapper to ensure consistent authorization handling."""
    if model is None:
        model = handler.__modelclass__
    if not handler.is_authorized(method=handler.request.method,
                                 model=model, instance=instance):
        raise exceptions.HTTPForbidden


class ModelAPI(JSONRequestHandler):
    __modelclass__ = None  # Subclasses should override this with an ndb.Model
    __apiname__ = None

    route_template_item = 'api/data/i/%s/<key:[^/]+>'
    route_template_collection = 'api/data/i/%s/'

    @classmethod
    def routes(cls, prefix='/'):
        """Construct a URL route (pattern) for this model class."""
        clsname = cls.__apiname__ or cls.__modelclass__._get_kind()

        yield webapp2.Route((prefix + cls.route_template_collection) % clsname,
                            handler=cls, name='data/%s/collection' % clsname)

        yield webapp2.Route((prefix + cls.route_template_item) % clsname,
                            handler=cls, name='data/%s/item' % clsname)

    @classmethod
    def register_routes(cls, app, prefix='/'):
        """Attach this class to a specific application."""
        assert isinstance(app, webapp2.WSGIApplication), \
            "Registration requires a webapp2.WSGIApplication instance"
        for route in cls.routes(prefix=prefix):
            app.router.add(route)

    @classmethod
    def model_url(cls, model=None, instance=None):
        """Retrieve a URL for a model (instance or key)."""
        if model is None:
            model = cls.__modelclass__
        if isinstance(instance, ndb.Model):
            name = ('data/%s/item' % instance._get_kind())
            kwargs = {'key': instance.key.urlsafe()}
        elif isinstance(instance, ndb.Key):
            name = ('data/%s/item' % instance.kind())
            kwargs = {'key': instance.urlsafe()}
        else:
            name = ('data/%s/collection' % model._get_kind())
            kwargs = {}
        return webapp2.uri_for(name, **kwargs)

    @property
    def model(self):
        return self.__modelclass__

    def fetch_model_instance(self, key, required=False):
        """Retireve the given key from datastore, with exception if invalid."""
        result = None
        if key:
            result = ndb.Key(urlsafe=key)
            # logging.info('Resolving key %r' % result)
            result = result.get()

        if (result is None) and required:
            raise exceptions.HTTPNotFound

        return result

    def is_authorized(self, method=None, model=None, instance=None):
        """
        Simple request authorization proxy.

        Subclasses should override this per model.
        """
        return True

    def prepare_query(self):
        """
        Construct a query from the given query.

        This will assemble a GQL query string from a notation similar to that
        of MongoDB.
        """
        return gql_query_request(self.request, self.__modelclass__)

    def present(self, item):
        """Coerce a datastore object to a JSON-compatible representation."""
        assert isinstance(item, ndb.Model), \
            "Require an NDB model for JSON coersion"
        result = item.to_dict()
        result['$key'] = item.key
        result['$url'] = self.model_url(instance=item)
        return result

    def retrieve_input(self, model):
        """Map a dictionary for properties of the model from the request."""
        values = {}
        for k, prop in model._properties.items():
            provided = self.request.input.get(k, None)
            if provided is not None:
                values[k] = provided
        return values

    def get(self, key=None):
        """Fetch a specific instance (or collection) representation."""
        # logging.info('Processing query for key %r' % key)
        assert_authorization(self)
        if key:
            item = self.fetch_model_instance(key, required=True)
            assert_authorization(self, instance=item)
            return self.response.write_json(self.present(item))
        else:
            query = self.prepare_query()
            return self.response.write_json([self.present(i) for i in query])

    def put(self, key=None):
        """Update a specific instance."""
        # Retrieve the item from datastore; raises 404 when missing.
        assert_authorization(self)
        item = self.fetch_model_instance(key, required=True)
        props = self.retrieve_input(self.__modelclass__)
        assert_authorization(self, instance=item)
        try:
            item.populate(**props)
            item.put()
            self.response.set_status(202, 'Accepted')
        except ValueError, e:
            message = 'Coersion failure [%s]' % e.message
            raise exceptions.HTTPUnprocessableEntity(message)

    def post(self, key=None):
        """Create a new instance."""
        if key:
            raise exceptions.HTTPBadRequest

        assert_authorization(self)
        props = self.retrieve_input(self.__modelclass__)

        try:
            item = self.__modelclass__(**props)
            key = item.put()
            self.response.set_status(201, 'Created')
            self.response.headers['Location'] = self.model_url(instance=key)
        except ValueError, e:
            message = 'Coersion failure [%s]' % e.message
            raise exceptions.HTTPUnprocessableEntity(message)

    def head(self, key=None):
        """Retrieve some metadata about the record."""
        assert_authorization(self)
        if key:
            item = self.fetch_model_instance(key, required=True)
            assert_authorization(self, instance=item)
            self.response.headers['X-Record-Exists'] = "true"
            self.response.set_status(200, 'OK')
        else:
            query = self.prepare_query()
            self.response.headers['X-Records-Match'] = query.count()
            self.response.set_status(200, 'OK')

    def delete(self, key=None):
        """Remove a record from this model."""
        assert_authorization(self)
        try:
            item = ndb.Key(urlsafe=key)
            if item is None:
                raise exceptions.HTTPNotFound
            assert_authorization(self, instance=item)
            item.delete()
            self.response.set_status(202, 'Accepted')
        except:
            raise exceptions.HTTPUnprocessableEntity


def api(model, name_override=None):
    """Construct a request handler class from an ndb.Model class."""
    assert issubclass(model, (ndb.Model, ndb.Expando)), \
        'JSON API requires a model.'

    bases = (ModelAPI, JSONRequestHandler)
    props = {'__modelclass__': model, '__apiname__': name_override}
    return type('JSONAPI_' + model.__name__, bases, props)
