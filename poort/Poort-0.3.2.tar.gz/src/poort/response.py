# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .utils import FileStorage
from decimal import Decimal
from jinja2.runtime import Undefined
from jinja2.exceptions import TemplateNotFound
from os import path
from pandora.compat import PY2
from pandora.compat import text_type
from time import mktime
from time import time
from werkzeug.datastructures import Headers
from werkzeug.http import dump_cookie
from werkzeug.http import http_date
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.http import is_resource_modified
from werkzeug.wsgi import wrap_file
from zlib import adler32
import datetime as dt
import jinja2
import json
import mimetypes


class Response(object):
    """A response wrapper.

    :param body: Body of the response.
    :param headers: Headers to respond with.
    :param status_code: Status-code of the response [default 200].

    :type body: str
    :type headers: werkzeug.datastructures.Headers | list
    :type status_code: int

    .. code-block:: python

        import poort

        def application(environ, start_response):
            request = poort.Request(environ)
            response = poort.Response('Hallo world!')

            return response(request, start_response)

    """

    def __init__(self, body='', headers=None, status_code=200):
        self.status_code = status_code
        self.headers = Headers(headers)
        self.body = body

    def get_status(self):
        """Get the status of the response as HTTP code.

        :rtype: str

        """

        return '{:d} {:s}'.format(self.status_code,
                                  HTTP_STATUS_CODES[self.status_code])

    def get_body(self):
        """Retrieve the body of the response.

        You can override this method to serialize JSON, for example,
        and return this as the body.

        :rtype: str

        """
        return self.body

    def prepare_response(self, request=None):
        """Prepare the response.

        This prepares (encodes) the body, you can override this method
        to add/override headers when the response is being prepared.

        To yield other content, you should look at `get_body`.

        :param request: Request that was made, None is allowed.

        :type request: poort.Request

        :rtype: str

        """
        if PY2:
            return [self.get_body().encode('utf-8')]
        else:
            return [bytes(self.get_body(), 'UTF8')]

    def respond(self, request):
        """Prepare a tuple to respond with.

        :param request: Request that was made, None is allowed.

        :type request: poort.Request

        :rtype: tuple[str, list[str], str]

        """
        response = self.prepare_response(request)
        return (self.get_status(), self.headers.to_wsgi_list(), response)

    def __call__(self, request, start_response):
        """Respond to WSGI with the current settings.

        :param request: Request that was made, None is allowed.
        :param start_response: Handler provided by WSGI.

        :type request: poort.Request
        :type start_response: callable

        """
        status, headers, response = self.respond(request)
        start_response(status, headers)
        return response

    def set_cookie(self, name, value='', max_age=None,
                   path='/', domain=None, secure=False, httponly=True):
        """Add a cookie to the response.

        :param name: Name of the cookie.
        :param value: Value of the cookie (should always be a string).
        :param max_age: Maximum age (leave `None` for "browser session").
        :param path: Path to bind the cookie to [default `'/'`].
        :param domain: Domain to bind the cookie to [default `None`].
        :param secure: Secure the cookie [default `False`],
            handy: `request.ssl`.
        :param httponly: Cookie not accessable by JavaScript [default `true`].

        :type name: str
        :type value: str
        :type max_age: int | None
        :type path: str
        :type domain: str | None
        :type secure: bool
        :type httponly: bool

        """
        self.headers.add('Set-Cookie', dump_cookie(
            name, value=str(value), max_age=max_age,
            path=path, domain=domain,
            secure=secure, httponly=httponly,
            charset='utf-8', sync_expires=True))

    def del_cookie(self, name, path='/', domain=None, secure=False,
                   httponly=True):
        """Delete a cookie from the browser.

        :param name: Name of the cookie.
        :param path: Path to bind the cookie to [default `'/'`].
        :param domain: Domain to bind the cookie to [default `None`].
        :param secure: Secure the cookie [default `False`],
            handy: `request.ssl`.
        :param httponly: Cookie not accessable by JavaScript [default `true`].

        :type name: str
        :type path: str
        :type domain: str | None
        :type secure: bool
        :type httponly: bool

        .. note::
            Take note that you must match the original settings of the cookie.
            Deleting a cookie with a non-matching path will not work.

        """
        self.set_cookie(name, max_age=0, path=path, domain=domain,
                        secure=secure, httponly=httponly)


class JsonResponse(Response):
    """A response wrapper for JSON results.

    Automaticly sets the *Content-Type* to `application/json` and transforms
    your data when the response is prepared. Override `json_default` to
    provide your own default transformations.

    It automaticly handles `datetime`, `date,`, `Decimal`, `FileStorage`,
    items with `.to_dict()`, items that can be iterated and items with
    `__str__`. When this fails, it simple calls `repr` on the item, it will
    not raise an Exception when it cannot handle formatting the item.

    :param data: Data to convert to JSON.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].

    :type data: dict
    :type status_code: int
    :type template_response_class: callable | None

    .. code-block:: python

        import poort

        def get_some_information():
            return poort.JsonResponse({
                'status': 'ok',
                'data': {
                    'some': 'Data here.'
                }
            })

    """

    def __init__(self, data, headers=None, status_code=200):
        self.data = data
        super(JsonResponse, self).__init__(headers=headers,
                                           status_code=status_code)
        self.headers.set('Content-Type', 'application/json')

    def get_body(self):
        return json.dumps(self.data, default=self.json_default)

    def json_default(self, value):
        if type(value) is Undefined:
            return None
        elif isinstance(value, (dt.datetime, dt.date)):
            return value.isoformat()
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, FileStorage):
            return value.filename
        elif hasattr(value, 'to_dict'):
            return value.to_dict()
        elif hasattr(value, '__iter__'):
            return [v for v in value]
        elif type(value).__str__ is not object.__str__:
            return text_type(value)
        else:
            return repr(value)


class HtmlResponse(Response):
    """A response wrapper for HTML results.

    Automaticly sets the *Content-Type* to `text/html`

    :param body: Your HTML data.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].

    :type body: str
    :type status_code: int
    :type template_response_class: callable | None

    .. code-block:: python

        import poort

        def get_some_information():
            return poort.HtmlResponse('''
                <html>
                    <head>
                        <title>Hello</title>
                    </head>
                    <body>
                        <p>Hello, this is some HTML.</p>
                    </body>
                </html>
            ''')

    """

    def __init__(self, body, headers=None, status_code=200):
        super(HtmlResponse, self).__init__(body, headers, status_code)
        self.headers.set('Content-Type', 'text/html')


class TemplateResponse(HtmlResponse):
    """A templated wrapper for HTML results.

    Automaticly sets the *Content-Type* to `text/html`. This uses the
    staticly bound `renderer` (a Jinja2 environment by default) to render
    your HTML.

    :param filename: Filename of the template.
    :param context: Context passed into the template.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].

    :type filename: str
    :type context: dict
    :type status_code: int
    :type template_response_class: callable | None

    :ivar jinja2.Environment renderer: Template renderer.

    .. code-block:: python

        import poort

        poort.TemplateResponse.configure('./templates')

        def get_some_information():
            return poort.TemplateResponse('index.html', {'name': 'World'})

    .. code-block:: html

        <!-- templates/index.html -->
        <html>
            <head>
                <title>Hallo</title>
            </head>
            <body>
                <p>Hallo {{ name }}!</p>
            </body>
        </html>

    """

    renderer = None

    def __init__(self, filename, context, headers=None, status_code=200):
        self.filename = filename
        self.context = context

        super(HtmlResponse, self).__init__(headers=headers,
                                           status_code=status_code)

    def get_template(self, filename=None):
        """Get a template from the renderer.

        :param filename: Get the template of `filename`
            [default `self.filename`].

        :type filename: str

        :rtype: jinja2.Template
        """
        return self.renderer.get_template(filename or self.filename)

    def render(self, context=None, filename=None):
        """Render a template.

        :param context: Context passed into the template.
        :param filename: Filename of the template [default `self.filename`].

        :type context: dict
        :type filename: str

        :rtype: str
        """
        if context is None:
            context = dict()

        return self.get_template(filename).render(**context)

    def get_body(self):
        return self.render(context=self.context)

    @classmethod
    def configure(cls, file_system_load_path='./templates', extensions=None):
        """Configure the class.

        This will instantiate the `renderer` variable with a Jinja2
        Environment.

        :param file_system_load_path: Where the templates are located.
        :param extensions: A list of Jinja2 extensions
            [defaults `do, loopcontrols, with_, autoescape`].

        :type file_system_load_path: str
        :type extensions: list[str]

        :rtype: jinja2.Environment
        """
        file_system_load_path = path.abspath(file_system_load_path)
        loader = jinja2.FileSystemLoader(file_system_load_path)

        extensions = extensions or [
            'jinja2.ext.do',
            'jinja2.ext.loopcontrols',
            'jinja2.ext.with_',
            'jinja2.ext.autoescape',
        ]

        cls.renderer = jinja2.Environment(loader=loader, extensions=extensions)
        return cls.renderer


class WrappedTemplateResponse(TemplateResponse):
    """A wrapping templated wrapper for HTML results.

    Automaticly sets the *Content-Type* to `text/html`. You can use this class
    to have a wrapper around your template. It extends `TemplateResponse` and
    works in the same manner, except it also renders a `base_template` and
    injects the rendered template into it as the `body`.

    :param filename: Filename of the template.
    :param context: Context passed into the template.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].
    :param base_template:

    :type filename: str
    :type as_attachment: bool | str
    :type cache_timeout: int
    :type headers: werkzeug.datastructures.Headers | list
    :type status_code: int

    .. code-block:: python

        import poort

        poort.WrappedTemplateResponse.configure('./templates')
        poort.WrappedTemplateResponse.BASE_TEMPLATE = 'base.html'

        def get_some_information():
            return poort.TemplateResponse('index.html', {
                'name': 'World',
                'scripts': ['/assets/scripts/jquery.min.js',
                            '/assets/scripts/bootstrap.min.js'],
                'styles': ['/assets/styles/bootstrap.min.css'],
            })

    .. code-block:: html

        <!-- templates/index.html -->
        {% do scripts.append('/assets/scripts/index.js') %}
        <p>Hallo {{ name }}!</p>

    .. code-block:: html

        <!-- templates/base.html -->
        <html>
            <head>
                <title>Hallo</title>

                {% for style in context.styles %}
                  <link href="{{ style }}" rel="stylesheet">
                {% endfor %}
            </head>
            <body>
                {{ body }}
                {% for script in context.scripts %}
                    <script src="{{ script }}">
                {% endfor %}
            </body>
        </html>

    .. note::

        This is a work-around for mutating *scripts* and *styles* (among
        other things) while rendering a page. By mutating the original
        context, the base template can use the *updated* variables. If you
        simply want to render templates without this functionality, simply use
        `TemplateResponse` as the simple extending result can be achieved
        using `{% extend 'base.html' %}`.

    """

    BASE_TEMPLATE = 'base.html'

    def __init__(self, template, context, headers=None, status_code=200,
                 base_template=None):
        self.base_template = base_template or self.BASE_TEMPLATE

        super(WrappedTemplateResponse, self).__init__(template, context,
                                                      headers, status_code)

    def get_body(self):
        return self.render(context={
            'body': self.render(context=self.context, filename=self.filename),
            'context': self.context,
        }, filename=self.base_template)


class FileResponse(Response):
    """A file wrapper response.

    This will send a file to the requester. The *Content-Type* will be
    guessed, it will also set the *Content-Length* and *Last-Modified*
    information based on the file.

    You can enable *caching* by providing the `request` when delivering the
    response and by setting the `cache_timeout`.

    :param filename: Filename you want to sent, absolute is preferred.
    :param as_attachment: Send the file as an attachment, `True` will
        use the basename of `filename`, set it to a `str`
        (`'download.csv'`) to determine the attachment name yourself.
    :param cache_timeout: How long should the result be cached
        [default `43200`, 12 hours).
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].

    :type filename: str
    :type as_attachment: bool | str
    :type cache_timeout: int
    :type headers: werkzeug.datastructures.Headers | list
    :type status_code: int

    :ivar str attachment_filename: Name of the attachment.

    .. code-block:: python

        import poort

        def get_some_information():
            return poort.FileResponse('cached-123456789-download.csv',
                                      'download-name-here.csv')

        def application(environ, start_response):
            request = poort.Request(environ)
            response = get_some_information()

            return response(request, start_response)

    .. seealso::

        For passing the `request` variable: :py:meth:`Response.__call__`

    """

    def __init__(self, filename, as_attachment=False,
                 cache_timeout=60 * 60 * 12, headers=None, status_code=200):
        if not path.exists(filename):
            raise ValueError('File `{:s}` does not exist.'.format(
                filename))

        super(FileResponse, self).__init__(headers=headers,
                                           status_code=status_code)
        self.filename = filename
        self.cache_timeout = cache_timeout
        self.as_attachment = bool(as_attachment)

        if as_attachment is True:
            self.attachment_filename = path.basename(self.filename)
        elif as_attachment:
            self.attachment_filename = as_attachment
        else:
            self.attachment_filename = None

    @property
    def size(self):
        """Size of the file in bytes.

        :rtype: int
        """
        return path.getsize(self.filename)

    @property
    def mtime(self):
        """Modified datetime of the file.

        :rtype: datetime.datetime
        """
        return dt.datetime.fromtimestamp(int(path.getmtime(self.filename)))

    @property
    def etag(self):
        """Get an Etag based on the file.

        :rtype: str
        """
        if PY2:
            filename = self.filename
        else:
            filename = bytes(self.filename, 'UTF8')

        return 'etag-%d-%s-%s' % (
            mktime(self.mtime.timetuple()),
            self.size,
            adler32(filename) & 0xffffffff
        )

    def prepare_response(self, request=None):
        if request is None:
            environ = dict()
        else:
            environ = request.environ

        guessed_type = mimetypes.guess_type(self.filename)
        mime_type = guessed_type[0] or 'text/plain'

        stream = open(self.filename)

        self.headers['Date'] = http_date()

        if self.cache_timeout and request:
            self.headers.extend((
                ('Etag', '"{:s}"'.format(self.etag)),
                ('Cache-Control', 'max-age={:d}, public'.format(
                    self.cache_timeout)),
            ))

            if not is_resource_modified(environ, self.etag):
                stream.close()
                self.status_code = 304
                return []

            self.headers['Expires'] = http_date(time() + self.cache_timeout)
        else:
            self.headers['Cache-Control'] = 'public'

        self.headers.extend((
            ('Content-Type', mime_type),
            ('Content-Length', str(self.size)),
            ('Last-Modified', http_date(self.mtime))
        ))

        if self.as_attachment:
            self.headers.set('Content-Disposition', 'attachment',
                             filename=self.attachment_filename)

        return wrap_file(environ, stream)


def template_or_json_response(request, template, context, headers=None,
                              status_code=200, template_response_class=None,
                              json_response_class=None):
    """Return a JSON or HTML response, based on the request.

    When called, it checks the **Request.want_json** variable.
    Based on this outcome a `template_response_class` or a
    `json_response_class` is spawned.

    :param request: Request of the caller.
    :param template: The filename of the template.
    :param context: Context that should be passed.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].
    :param template_response_class: Which template response class should be
        used [default :class:`TemplateResponse`].
    :param json_response_class: Which JSON response class should be
        used [default :class:`JsonResponse`].

    :type request: poort.Request
    :type template: str
    :type context: dict
    :type headers: werkzeug.datastructures.Headers | list
    :type status_code: int
    :type template_response_class: callable | None
    :type json_response_class: callable | None

    .. code-block:: python

        import poort
        import poort.template_or_json_response as toj

        def get_some_information(request):
            return toj(request, 'user.html', {
                'id': 44,
                'email': 'j.doe@example.com',
                'first': 'John',
                'last': 'Doe',
            })

        def application(environ, start_response):
            request = poort.Request(environ)
            response = get_some_information(request)

            return response(request, start_response)

    """

    if template_response_class is None:
        template_response_class = TemplateResponse
    if json_response_class is None:
        json_response_class = JsonResponse

    trc = template_response_class
    jrc = json_response_class

    if request.want_json:
        return jrc(context, headers, status_code)
    else:
        try:
            return trc(template, context, headers, status_code)
        except TemplateNotFound:
            return jrc(context, headers, status_code)


def wrapped_template_or_json_response(request, template, context, headers=None,
                                      status_code=200,
                                      template_response_class=None,
                                      json_response_class=None):
    """Return a JSON or HTML response, based on the request.

    When called, it checks the **Request.want_json** variable.
    Based on this outcome a `template_response_class` or a
    `json_response_class` is spawned.

    :param request: Request of the caller.
    :param template: The filename of the template.
    :param context: Context that should be passed.
    :param headers: A list of extra headers, be warned that some headers
        may be overridden.
    :param status_code: Status-Code of the response [default `200`].
    :param template_response_class: Which template response class should be
        used [default :class:`WrappedTemplateResponse`].
    :param json_response_class: Which JSON response class should be
        used [default :class:`JsonResponse`].

    :type request: poort.Request
    :type template: str
    :type context: dict
    :type headers: werkzeug.datastructures.Headers | list
    :type status_code: int
    :type template_response_class: callable | None
    :type json_response_class: callable | None

    .. code-block:: python

        import poort
        import poort.wrapper_template_or_json_response as wtoj

        def get_some_information(request):
            return wtoj(request, 'user.html', {
                'id': 44,
                'email': 'j.doe@example.com',
                'first': 'John',
                'last': 'Doe',
            })

        def application(environ, start_response):
            request = poort.Request(environ)
            response = get_some_information(request)

            return response(request, start_response)

    """

    if template_response_class is None:
        template_response_class = WrappedTemplateResponse
    if json_response_class is None:
        json_response_class = JsonResponse

    return template_or_json_response(request, template, context, headers,
                                     status_code, template_response_class,
                                     json_response_class)
