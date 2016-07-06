# Copyright 2013-2016 Juca Crispim <juca@poraodojuca.net>

# This file is part of pyrocumulus.

# pyrocumulus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyrocumulus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyrocumulus.  If not, see <http://www.gnu.org/licenses/>.

import os
from mongomotor import Document, EmbeddedDocument
from mongomotor.queryset import QuerySetManager, QuerySet
from tornado import gen
from tornado.concurrent import Future
from tornado.web import RequestHandler, HTTPError
from tornado.web import StaticFileHandler as StaticFileHandlerTornado
from pyrocumulus.utils import get_value_from_settings, fqualname, import_class
from pyrocumulus.converters import get_converter, get_request_converter
from pyrocumulus.parsers import get_parser
from pyrocumulus.exceptions import (PyrocumulusException, StaticFileError,
                                    PyrocumulusConfusionError)
from pyrocumulus.web import decorators
from pyrocumulus.web.metaclasses import HandlerOperationMetaclass
from pyrocumulus.web.mixins import (BasicAPIKeyAuthMixin,
                                    RestAPIAuthMixin, ReadOnlyMixin)
from pyrocumulus.web.template import render_template


class PyroRequest:
    """Class that parses the incomming request. """

    def __init__(self, request):
        self.base_request = request
        self.new_request = self._decode_values(self.base_request)

    def __delitem__(self, key):
        del self.new_request[key]

    def _decode_values(self, request):
        new_req = {}
        for k, v in request.items():
            new_req[k] = [vv.decode() for vv in v]
        return new_req

    def keys(self):
        """Returns the request keys"""
        return self.new_request.keys()

    def get(self, key):
        """Returns a single value for a key. If it's not present
        returns None."""
        return self.new_request.get(key, [None])[0]

    def getlist(self, key):
        """Returns a list of values for a key. If it's not preset
        returns an empyt list."""
        return self.new_request.get(key, [])


class BasePyroHandler(RequestHandler, metaclass=HandlerOperationMetaclass):
    """Base handler for all pyrocumulus handlers. Responsible for
    enable cors."""

    def initialize(self, cors_origins=None):
        """Called after constructor. Handle cors.

        :param cors_origins: Value to "Access-Control-Allow-Origin" header.
          If not cors_origin, cors is disabled."""

        self.params = None
        self.cors_origins = cors_origins
        self.cors_enabled = True if self.cors_origins else False
        if self.cors_enabled:
            self._enable_cors()

    # Making it a coro to keep everything the same
    @gen.coroutine
    def prepare(self):
        self.params = PyroRequest(self.request.arguments)

    def __getattribute__(self, attrname):

        if attrname in ['get', 'post', 'put', 'delete']:
            return self.validate_and_run
        elif attrname == 'options':
            return self.validate_options
        else:
            return super().__getattribute__(attrname)

    def _enable_cors(self):
        allowed_methods = 'GET, PUT, POST, DELETE, OPTIONS'
        self.set_header("Access-Control-Allow-Origin", self.cors_origins)
        self.set_header("Access-Control-Allow-Credentials", 'true')
        self.set_header("Access-Control-Allow-Methods", allowed_methods)
        self.set_header('Access-Control-Allow-Headers', '*')

    def get_allowed_operations(self):
        """Returns a set with all allowed operations for this handler."""

        return self.operation_mapper.get_all_operations_for(
            fqualname(type(self)))

    @gen.coroutine
    def write_response(self, chunk):
        # making it a coroutine so subclasses can use coroutines
        # on their write_response
        self.write(chunk)

    @gen.coroutine
    def validate_and_run(self, operation):
        """Validates the incomming request and proceeds with that if valid."""

        meth2call = self.operation_mapper.validate(fqualname(type(self)),
                                                   self.request.method.lower(),
                                                   operation)

        returned_obj = meth2call(self)
        if isinstance(returned_obj, Future):
            returned_obj = yield returned_obj

        yield self.write_response(returned_obj)

    def validate_options(self, operation):
        """Validates options requests. If ``operation`` exists for any
        request method, so it is a valid operation for options."""

        if operation not in self.get_allowed_operations():
            raise HTTPError(404)

        return self.send_options()

    @decorators.options('')
    def send_options(self):
        if not self.cors_origins:
            return {'corsEnabled': False}

        self._enable_cors()
        self.write({'corsEnabled': True})


class BasePyroAuthHandler(BasicAPIKeyAuthMixin, BasePyroHandler):
    """BasePyroHandler with authentication."""


class ModelHandler(BasePyroHandler):

    """
    Base request handler for all handlers used
    for automatic api creation.
    """

    def initialize(self, model, cors_origins=None):
        """
        Method called after the class' constructor. Initializes
        the model and parses it.

        :param model: mongomotor Document subclass
        :param cors_origin: Value to "Access-Control-Allow-Origin" header.
                            If not cors_origin, cors is disabled.
        """
        self.model = model
        super(ModelHandler, self).initialize(cors_origins=cors_origins)

    @gen.coroutine
    def prepare(self):
        """
        Method called in the beginnig of every request.
        Initializes the params to be passed to self.model.objects.
        """
        self.params = yield self._prepare_arguments()

    @gen.coroutine
    def _prepare_arguments(self):
        """
        Parse request params and create dict containing
        only params to be passed to mongomotor queryset
        get() or filter()
        """
        converter = get_request_converter(self.request.arguments, self.model)
        mydict = yield converter.to_dict()
        return mydict

    @classmethod
    def embeddedhandler(cls):  # pragma no cover
        """
        Returns the request handler for embedded documents
        """

        raise NotImplementedError


class RestHandler(ModelHandler):

    """
    Request handler for rest applications
    """

    def initialize(self, model, object_depth=1, *args, **kwargs):
        """
        :param model: mongomotor Document subclass.
        :param object_depth: depth of the object, meaning how many
          levels of RelatedFields will be returned. Defaults to 1.

        Initializes object_depth.
        """
        super(RestHandler, self).initialize(model, *args, **kwargs)
        self.object_depth = object_depth
        self.json_extra_params = {}
        self.order_by = None
        self.pagination = None

    @gen.coroutine
    def prepare(self):
        """
        Initializes json_extra_params which will be update()'d into
        the response json and get its pagination info needed for
        listing things and all model related stuff.
        """
        self.order_by = self._get_order_by()
        self.pagination = self._get_pagination()
        yield super(RestHandler, self).prepare()

        self.parser = get_parser(self.model)
        self.parsed_model = self.parser.parse()
        self.model_reference_fields = self.parsed_model['reference_fields']
        self.model_embedded_documents = self.parsed_model['embedded_documents']
        self.model_list_fields = self.parsed_model['list_fields']

    @gen.coroutine
    def write_response(self, returned_obj):
        """
        Formats and write ``returned_obj``

        :param returned_obj: The return value of the method that handled
          the operation.
        """

        if isinstance(returned_obj, str):
            to_return = returned_obj
        else:
            to_return = yield self._get_clean_dict(returned_obj)
            to_return.update(self.json_extra_params)

        self.write(to_return)

    @classmethod
    def embeddedhandler(cls):
        return EmbeddedDocumentHandler

    def get_list_queryset(self, **kwargs):
        """ Returns a queryset filtered by ``kwargs`` and
        sorted by ``self.order_by``."""

        clean_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, list):
                value = value[0]
            clean_kwargs[key] = value

        objects = self.model.objects.filter(**clean_kwargs)
        for order in self.order_by:
            objects = objects.order_by(order.decode())

        return objects

    @decorators.get('doc')
    def show_documentation(self):
        """Shows a documentation about the document type being handled."""

        cls_name = self.model.__name__
        tmpl = """{cls_name}<br/><br/>""".format(cls_name=cls_name)
        for field in self.parser.fields:
            if field['name'] == 'id':
                continue
            field_name = field['name']
            field_type = field['type'].__class__.__name__
            required = field['required']
            primary_key = field['primary_key']
            unique = field['unique']

            tmpl += """{field_name} = {field_type}<br/>""".format(
                field_name=field_name, field_type=field_type)

            if primary_key:  # pragma no cover
                tmpl += "&nbsp;&nbsp;- primary key<br/>"
            if required:  # pragma no cover
                tmpl += "&nbsp;&nbsp;- required<br/>"
            if unique:  # pragma no cover
                tmpl += '&nbsp;&nbsp;- unique<br/>'

            tmpl += '<br/>'
        return tmpl

    @decorators.get('')
    @gen.coroutine
    def get_or_list(self):
        """Returns a specific object os a list of objects. If has
        a primary key in the request params returns a specific object
        otherwise returns a list of objects."""

        if self._params_has_pk():
            r = yield self.get_object()
        else:
            r = yield self.list_objects()

        return r

    @gen.coroutine
    def list_objects(self):
        """
        Method that returns a list of objects.
        """
        objects = self.get_list_queryset(**self.params)

        total_items = yield objects.count()
        extra = {'total_items': total_items}
        self.json_extra_params.update(extra)
        return (yield objects[self.pagination['ini']:self.pagination['end']])

    @gen.coroutine
    def get_object(self, **kwargs):
        """
        Returns a single object.
        """
        obj = yield self.model.objects.get(**self.params)
        return obj

    @decorators.post('')
    @gen.coroutine
    def insert_object(self, **kwargs):
        """Creates an object in the database. Called by
        post (). """
        obj = self.model(**self.params)
        yield obj.save()
        return obj

    @decorators.put('')
    @gen.coroutine
    def put_object(self):
        """
        Updates an object in the database. Called by
        put().
        """
        if not self._params_has_pk():
            raise HTTPError(500)

        pk_fields = [f.name for f in self.model._lookup_field('pk')]
        upsert_kw = {'set__{}'.format(k): v for k, v in self.params.items()
                     if k not in pk_fields}
        upsert_kw.update({f: self.params[f] for f in pk_fields})
        updated = yield self.model.objects.update_one(**upsert_kw)

        if not updated:
            raise HTTPError(404)
        return self.params

    @decorators.delete('')
    @gen.coroutine
    def delete_object(self, **kwargs):
        """
        deletes an object. Called by delete()
        """

        obj = yield self.get_object(**self.params)
        yield obj.delete()

        return {'id': str(obj.id)}

    def _params_has_pk(self):
        """Check if in the request params has pk fields."""

        pk_fields = [f.name for f in self.model._lookup_field('pk')]
        for pk_field in pk_fields:
            if self.params.get(pk_field):
                return True
        return False

    @gen.coroutine
    def _get_clean_dict(self, obj):
        """
        Returns a dict ready to serialize. Use pyrocumulus.converters
        to do that.
        """
        if (isinstance(obj, Document)
                or isinstance(obj, EmbeddedDocument)
                or isinstance(obj, QuerySetManager)
                or isinstance(obj, QuerySet)):

            converter = get_converter(obj, max_depth=self.object_depth)
            mydict = yield converter.to_dict()
            mydict = converter.sanitize_dict(mydict)

        elif isinstance(obj, dict):
            mydict = obj

        elif isinstance(obj, list):
            mylist = []
            for o in obj:
                clean_obj = yield self._get_clean_dict(o)
                mylist.append(clean_obj)

            mylist = [i for i in mylist]
            mydict = {'items': mylist,
                      'quantity': len(obj)}
        else:
            msg = """'I\'m confused. I don\'t know what to do with a {}.'"""
            msg += """Return a dict from your method."""
            raise PyrocumulusConfusionError(msg.format(type(obj)))

        return mydict

    def _get_pagination(self):
        """
        Get pagination parameters from requets' arguments
        """
        max_items = int(self.request.arguments.get('max', [10])[0])
        page = int(self.request.arguments.get('page', [1])[0])
        try:
            del self.request.arguments['max']
        except KeyError:
            pass
        try:
            del self.request.arguments['page']
        except KeyError:
            pass
        ini = (page - 1) * max_items
        end = ini + max_items
        pagination = {'ini': ini, 'end': end, 'max': max_items, 'page': page}
        return pagination

    def _get_order_by(self):
        order_by = self.request.arguments.get('order_by', [])

        try:
            del self.request.arguments['order_by']
        except KeyError:
            pass
        return order_by


class AuthRestHandler(RestAPIAuthMixin, RestHandler):

    """ Handler for authenticated APIs
    """
    pass


class ReadOnlyRestHandler(ReadOnlyMixin, RestHandler):

    """ Handler for read-only public APIs
    """
    pass


class EmbeddedDocumentHandler(RestHandler):

    def initialize(self, parent_doc, model, object_depth=1, *args, **kwargs):
        super(EmbeddedDocumentHandler, self).initialize(model, object_depth)
        self.parent_doc = parent_doc

    @gen.coroutine
    def prepare(self):
        yield super(EmbeddedDocumentHandler, self).prepare()
        self.parent_id = self._get_parent_id()
        del self.params['parent_id']
        self.parent = yield self.parent_doc.objects.get(id=self.parent_id)
        parser = get_parser(self.parent_doc)
        self.parsed_parent = parser.parse()

    @decorators.post('')
    @gen.coroutine
    def put_object(self, **kwargs):

        embed = self.model(**kwargs)
        field_name = self._get_field_name()
        # if its a listfield, verify if has something
        # already in list. If not, create a new one.

        if self.parsed_parent.get('list_fields') and \
           self.model in self.parsed_parent.get('list_fields').values():

            list_values = getattr(self.parent, field_name)
            if list_values:
                list_values.append(embed)
            else:
                list_values = [embed]
            setattr(self.parent, field_name, list_values)
        # if its not a list, set the object as the attribute
        else:
            setattr(self.parent, field_name, embed)

        yield self.parent.save()
        return embed

    @decorators.get('')
    @gen.coroutine
    def list_objects(self, **kwargs):
        field_name = self._get_field_name()
        objects_list = getattr(self.parent, field_name)
        total_items = len(objects_list)
        extra = {'total_items': total_items}
        self.json_extra_params.update(extra)
        r = objects_list[self.pagination['ini']:self.pagination['end']]
        return r

    @classmethod
    def embeddedhandler(cls):
        return cls

    def _get_parent_id(self):
        try:
            parent_id = self.request.arguments['parent_id'][0].decode()
        except (KeyError, IndexError):
            raise HTTPError(500, 'parent_id param is required')
        del self.request.arguments['parent_id']
        return parent_id

    def _get_field_name(self):
        """
        Returns the field name for this embedded document
        in the parent_doc
        """

        if self.parsed_parent.get('list_fields'):
            for key, value in self.parsed_parent.get('list_fields').items():
                if value == self.model:
                    return key

        if self.parsed_parent.get('embedded_documents'):
            for key, value in self.parsed_parent.get(
                    'embedded_documents').items():
                if value == self.model:
                    return key


class AuthEmbeddedDocumentHandler(RestAPIAuthMixin, EmbeddedDocumentHandler):
    pass


class ReadOnlyEmbeddedDocumentHandler(ReadOnlyMixin, EmbeddedDocumentHandler):
    pass


class StaticFileHandler(StaticFileHandlerTornado):

    """
    Handler for static files
    """

    def initialize(self, static_dirs, default_filename=None):
        self.root = None
        type(self).static_dirs = static_dirs
        self.default_filename = default_filename

    @classmethod
    def get_absolute_path(cls, root, path):
        """
        Returns the absolute path for a requested path.
        Looks in settings.STATIC_DIRS directories and returns
        the full path using the first directory in which ``path``
        was found.
        """
        if not cls.static_dirs:
            raise StaticFileError('No STATIC_DIRS supplied')

        for root in cls.static_dirs:
            cls.static_root = root
            abspath = os.path.abspath(os.path.join(root, path))
            if os.path.exists(abspath):
                break
        return abspath

    def validate_absolute_path(self, root, absolute_path):
        self.root = self.static_root
        return super(StaticFileHandler, self).validate_absolute_path(
            self.root, absolute_path)


class TemplateHandler(RequestHandler):

    """
    Handler with little improved template support
    """

    def render_template(self, template, extra_context):
        """
        Renders a template using
        :func:`pyrocumulus.web.template.render_template`.
        """
        self.write(render_template(template, self.request, extra_context))


def get_rest_handler(obj, parent=None, auth=False, readonly=False):
    """ Retuns a RequestHandler for a REST api for a given object
    :param obj: Document or EmbeddedDocument subclass
    :param parent: Parent Document to an EmbeddedDocument
    :param auth: Bool indicating if auth should be used.
    :param readonly: Bool indicating if the api is read only or not.
    """
    handler = None

    if issubclass(obj, Document):
        handler = _get_document_rest_handler(obj, auth, readonly)

    elif issubclass(obj, EmbeddedDocument):
        if not parent:
            raise PyrocumulusException(
                'a parent is needed for an EmbeddedDocument')

        handler = _get_embedded_document_rest_handler(
            obj, parent, auth, readonly)

    if not handler:
        raise PyrocumulusException('rest handler not found for %s' % str(obj))

    return handler


def _get_document_rest_handler(obj, auth, readonly):
    handler_class = None
    obj_fqualname = fqualname(obj)
    rest_handlers = get_value_from_settings('REST_HANDLERS', {})
    if auth:
        handler_class = get_value_from_settings('DEFAULT_AUTH_REST_HANDLER')
        handler = AuthRestHandler
    elif readonly:
        handler_class = get_value_from_settings(
            'DEFAULT_READ_ONLY_REST_HANDLER')
        handler = ReadOnlyRestHandler
    else:
        handler_class = get_value_from_settings('DEFAULT_REST_HANDLER')
        handler = RestHandler

    handler_class = rest_handlers.get(obj_fqualname) or handler_class

    if handler_class:
        handler = import_class(handler_class)

    return handler


def _get_embedded_document_rest_handler(obj, parent, auth, readonly):
    handler_class = None
    obj_fqualname = fqualname(obj)
    rest_handlers = get_value_from_settings('REST_HANDLERS', {})
    if auth:
        handler_class = get_value_from_settings(
            'DEFAULT_EMBEDDED_AUTH_REST_HANDLER')
        handler = AuthEmbeddedDocumentHandler
    elif readonly:
        handler_class = get_value_from_settings(
            'DEFAULT_READ_ONLY_EMBEDDED_REST_HANDLER')
        handler = ReadOnlyEmbeddedDocumentHandler
    else:
        handler_class = get_value_from_settings(
            'DEFAULT_EMBEDDED_REST_HANDLER')
        handler = EmbeddedDocumentHandler

    handler_class = rest_handlers.get(obj_fqualname) or handler_class

    if handler_class:
        handler = import_class(handler_class)

    return handler
