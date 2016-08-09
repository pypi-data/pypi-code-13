"""
Magic

"""

import re
import os
import sys
import inspect
import datetime
import functools
import logging
import logging.config
import copy
from six import string_types
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from werkzeug.exceptions import Aborter
from werkzeug import import_string
from flask import (Flask, g, render_template, flash, session, make_response,
                   Response, request,
                   url_for as f_url_for, redirect as f_redirect)
from flask_assets import Environment
import jinja2
from importlib import import_module
from . import utils
from . import exceptions
from .__about__ import *

_py2 = sys.version_info[0] == 2
# ------------------------------------------------------------------------------

__all__ = [
            "Magic",
            "MagicWand",
            "MagicError",
            "models",
            "views",
            "get_env",
            "set_env",
            "get_env_app",
            "get_env_config",
            "get_config",
            "page_meta",
            "abort",
            "flash_success",
            "flash_error",
            "flash_data",
            "get_flashed_data",
            "init_app",
            "register_app",
            "register_models",
            "import_module",

            # For convenience when importing from flask_magic, but can use
            # the flask one
            "flash",
            "session",
            "url_for",
            "request",
            "redirect",
           ]


# Will hold models/db from apps, or to be shared
# ie, set new model property -> models.MyNewModel = MyModel
# ie: use property -> models.MyNewModel.all()
# For conveniece, use `register_models(**kw)` to register the model
models = type('', (), {})


def register_models(**kwargs):
    """
    Alias to register models
    :param kwargs:
    :return:
    """
    [setattr(models, k, v) for k, v in kwargs.items()]


# Will hold all active class views
# It can be used for redirection etc
# ie: redirect(views.ContactPage.index)
views = type('', (), {})


__ENV__ = None


def set_env(env):
    """
    Set the envrionment manually
    :param env:
    :return:
    """
    global __ENV__
    __ENV__ = env.lower().capitalize()


def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str Capitalized
    """
    if not __ENV__:
        env = os.environ["env"] if "env" in os.environ else "Development"
        set_env(env)
    return __ENV__


def get_env_app():
    """
    Return the environ application name
    when it is passed in the environment as: app=app_name or app=app_name:environment
    ie: app=www:development or app=www
    :return: string
    """
    return get_environ_app()[0]


def get_environ_app():
    """
    if the app and the envi are passed in the command line as 'app=app:env'
    :return: tuple app, env
    """
    app, env = None, None
    if "app" in os.environ:
        appenv = os.environ["app"]
        if ":" in appenv:
            app, env = os.environ["app"].split(":")
            set_env(env)
        else:
            app = appenv
    return app.lower() if app else None, get_env()


def get_env_config(config):
    """
    Return config class based based on the config
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())


def init_app(kls):
    """
    To bind middlewares, plugins that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, "__call__"):
        raise TypeError("init_app: '%s' is not callable" % kls)
    Magic._init_apps.add(kls)
    return kls


def register_app(pkg):
    """
    Allow to register an app packages by loading and exposing: templates, static,
    and exceptions for abort()

    Structure of package
        root
            | $package_name
                | __init__.py
                |
                | exceptions.py
                |
                | /templates
                    |
                    |
                |
                | /static
                    |
                    | assets.yml

    :param pkg: str - __package__
                    or __name__
                    or The root dir
                    or the dotted resource package (package.path.path,
                    usually __name__ of templates and static
    """

    root_pkg_dir = pkg
    if not os.path.isdir(pkg) and "." in pkg:
        root_pkg_dir = utils.get_pkg_resources_filename(pkg)

    template_path = os.path.join(root_pkg_dir, "templates")
    static_path = os.path.join(root_pkg_dir, "static")

    logging.info("Registering App: " + pkg)
    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        Magic._template_paths.add(template_path)

    if os.path.isdir(static_path):
        Magic._static_paths.add(static_path)
        Magic._add_asset_bundle(static_path)

    if os.path.isfile(os.path.join(root_pkg_dir, "exceptions.py")):
        exceptions = utils.import_string(pkg + ".exceptions")
        init_app(lambda x: abort.map_from_module(exceptions))


def get_config(key, default=None):
    """
    Shortcut to access the application's config in your class
    :param key: The key to access
    :param default: The default value when None
    :returns mixed:
    """
    return Magic._app.config.get(key, default)


def page_meta(**kwargs):
    """
    Meta allows you to add page meta data
    :params **kwargs:

    meta keys we're expecting:
        title (str)
        description (str)
        url (str) (Will pick it up by itself if not set)
        image (str)
        site_name (str) (but can pick it up from config file)
        object_type (str)
        keywords (list)
        locale (str)
        card (str)

        **Boolean By default these keys are True
        use_opengraph
        use_twitter
        use_googleplus
python
    """
    meta = Magic._global.get("__META__", {})
    meta.update(**kwargs)
    Magic.g(__META__=meta)


def flash_success(msg):
    """
    Alias to flash, but set a success message
    :param msg:
    :return:
    """
    return flash(msg, "success")


def flash_error(msg):
    """
    Alias to flash, but set an error message
    :param msg:
    :return:
    """
    return flash(msg, "error")


def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session["_flash_data"] = data


def get_flashed_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop("_flash_data", None)


is_method = lambda x: inspect.ismethod if _py2 else inspect.isfunction


def url_for(endpoint, **kw):
    """
    Magic url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """

    _endpoint = None
    if isinstance(endpoint, string_types):
        return f_url_for(endpoint, **kw)

    else:
        # self, will refer the caller method, by getting the method name
        if isinstance(endpoint, Magic):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
            
        if is_method(endpoint):
            if hasattr(endpoint, "_rule_cache"):
                rc = endpoint._rule_cache
                if rc:
                    k = list(rc.keys())[0]
                    rules = rc[k]
                    len_rules = len(rules)
                    if len_rules == 1:
                        rc_kw = rules[0][1]
                        methods = rc_kw.get("methods", None)
                        if methods and ("GET" not in methods or "POST" not in methods):
                            raise MagicError("Magic `url_for` requires endpoint to have a GET or POST method")

                        _endpoint = rc_kw.get("endpoint", None)
                        if not _endpoint:
                            _endpoint = _build_endpoint_route_name(endpoint)

                    elif len_rules > 1:
                        _prefix = _build_endpoint_route_name(endpoint)
                        for r in Magic._app.url_map.iter_rules():
                            if ('GET' in r.methods or 'POST' in r.methods) \
                                    and _prefix in r.endpoint:
                                _endpoint = r.endpoint
                                break
            else:
                _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_url_for(_endpoint, **kw)
    else:
        raise MagicError('Magic `url_for` received an invalid endpoint')


def redirect(endpoint, **kw):
    """
    Redirect allow to redirect dynamically using the classes methods without
    knowing the right endpoint.
    Expecting all endpoint have GET as method, it will try to pick the first
    match, based on the endpoint provided or the based on the Rule map_url

    An endpoint can also be passed along with **kw

    An http: or https: can also be passed, and will redirect to that site.

    example:
        redirect(self.hello_world)
        redirect(self.other_page, name="x", value="v")
        redirect("https://google.com")
        redirect(views.ContactPage.index)
    :param endpoint:
    :return: redirect url
    """

    _endpoint = None

    if isinstance(endpoint, string_types):
        _endpoint = endpoint
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return f_redirect(endpoint)
        else:
            for r in Magic._app.url_map.iter_rules():
                if 'GET' in r.methods and endpoint in r.endpoint:
                    _endpoint = r.endpoint
                    break
                else:
                    return f_redirect(endpoint)
    else:
        # self, will refer the caller method, by getting the method name
        if isinstance(endpoint, Magic):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)

        if is_method(endpoint):
            if hasattr(endpoint, "_rule_cache"):
                rc = endpoint._rule_cache
                if rc:
                    k = list(rc.keys())[0]
                    rules = rc[k]
                    len_rules = len(rules)
                    if len_rules == 1:
                        rc_kw = rules[0][1]
                        methods = rc_kw.get("methods", None)
                        if methods and "GET" not in methods:
                            raise MagicError("Magic `redirect` requires endpoint to have a GET method")

                        _endpoint = rc_kw.get("endpoint", None)
                        if not _endpoint:
                            _endpoint = _build_endpoint_route_name(endpoint)

                    elif len_rules > 1:
                        _prefix = _build_endpoint_route_name(endpoint)
                        for r in Magic._app.url_map.iter_rules():
                            if 'GET' in r.methods and _prefix in r.endpoint:
                                _endpoint = r.endpoint
                                break
            else:
                _endpoint = _build_endpoint_route_name(endpoint)

    if _endpoint:
        return f_redirect(f_url_for(_endpoint, **kw))
    else:
        raise MagicError('Magic `redirect` received an invalid endpoint')


def _build_endpoint_route_name(endpoint):

    cls = endpoint.im_class() \
        if (not hasattr(endpoint, "__self__") or endpoint.__self__ is None) \
        else endpoint.__self__

    return cls.build_route_name(endpoint.__name__)


_method_cache_enpoints = None
def _build():
    pass

# ------------------------------------------------------------------------------

# https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/exceptions.py
class CustomAborter(Aborter):
    """
    We'll modify abort, to also use the name of custom HTTPException classes
    """

    def __call__(self, code, *args, **kwargs):
        if isinstance(code, string_types) and code in self.mapping:
            raise self.get_exception(code)(*args, **kwargs)
        super(CustomAborter, self).__call__(code, *args, **kwargs)

    def get_exception(self, code):
        """
        Expose the class based on the code
        :param code:
        :return:
        """
        raise self.mapping[code]

    def map_from_module(self, module):
        """
        Map all classes the in $module with subclasses of exceptions.HTTPException
        to be called as as error in with abort()
        :param obj:
        :return:
        """
        maps = {}
        for name in dir(module):
            obj = getattr(module, name)
            try:
                if issubclass(obj, exceptions.HTTPException):
                    maps[name] = obj
            except TypeError as ter:
                pass
        self.mapping.update(maps)

abort = CustomAborter()
abort.map_from_module(exceptions)

# ------------------------------------------------------------------------------

#
class Magic(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    Credit: Shout out to Flask-Classy for the greatest logic in this class
    Flask-Classy -> https://github.com/apiguy/flask-classy
    """

    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    base_layout = "layout.html"
    assets = None
    logger = None
    __special_methods = ["get", "put", "patch", "post", "delete", "index"]
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_meta = dict(
            title="",
            description="",
            url="",
            image="",
            site_name="",
            object_type="article",
            locale="",
            keywords=[],
            use_opengraph=True,
            use_googleplus=True,
            use_twitter=True,
            properties={}
        )
    _global = dict(
        __NAME__=__title__,
        __VERSION__=__version__,
        __YEAR__=datetime.datetime.now().year,
        __META__=_default_page_meta
    )

    @classmethod
    def __call__(cls,
                 flask_or_import_name,
                 project=None,
                 directory=None,
                 config=None,
                 exceptions=None,
                 compress_html=True,
                 exclude_views=False,
                 exclude_static=False,
                 exclude_templates=False,
                 load_installed_apps=True):
        """
        Allow to register all subclasses of Magic at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param project: name of the project. If the directory and config is empty, it will guess them from here
        :param directory: The directory containing your project's Views, Templates and Static
        :param config: string of config object. ie: "app.config.Dev"
        :param exceptions: The exceptions path to load
        :param compress_html: bool - If true it will use the plugin "htmlcompress"
                to remove white spaces off the html result
        :param exclude_views: bool - If true, it will setup everything but registering the views
        :param exclude_static: bool - If true, it will setup everything but registering the static
        :param exclude_templates: bool - If true, it will setup everything but registering the templates
        :param load_installed_apps: bool - When True it will load the installed apps
        """

        if isinstance(flask_or_import_name, Flask):
            app = flask_or_import_name
        else:
            app = Flask(flask_or_import_name)

        app.wsgi_app = ProxyFix(app.wsgi_app)

        app.url_map.converters['regex'] = RegexConverter

        if not directory:
            directory = "application/%s" % project if project else "."

        if not config:
            config = "application.config.%s" % get_env()

        app.config.from_object(config)

        # Extensions to remove extra white spaces in html
        if compress_html:
            app.jinja_env.add_extension('flask_magic.htmlcompress.HTMLCompress')

        if directory:
            app.template_folder = directory + "/templates"
            app.static_folder = directory + "/static"

        if exceptions:
            abort.map_from_module(exceptions)

        cls._app = app

        cls._setup_logger()

        if not exclude_static:
            cls._add_asset_bundle(app.static_folder)

        # Flask Assets
        cls.assets = Environment(cls._app)

        # INSTALLED_APPS
        if load_installed_apps:
            _ = cls.setup_installed_apps()

        # Setup init_app
        [_app(cls._app) for _app in cls._init_apps]

        # Register templates
        if not exclude_templates:
            if cls._template_paths:
                loader = [cls._app.jinja_loader] + list(cls._template_paths)
                cls._app.jinja_loader = jinja2.ChoiceLoader(loader)

        # Register static
        if not exclude_static:
            if cls._static_paths:
                cls.assets.load_path = [cls._app.static_folder] + list(cls._static_paths)
                [cls.assets.from_yaml(a) for a in cls._asset_bundles]

        # Register views
        if not exclude_views:
            for subcls in cls.__subclasses__():
                base_route = subcls.base_route
                if not base_route:
                    base_route = utils.dasherize(utils.underscore(subcls.__name__))
                    if subcls.__name__.lower() == "index":
                        base_route = "/"
                subcls._register(cls._app, base_route=base_route)


        @cls._app.after_request
        def _after_request_cleanup(response):
            cls._global["__META__"] = cls._default_page_meta.copy()
            return response
        return cls._app

    @classmethod
    def setup_installed_apps(cls):
        """
        To import applications along with associated properties

        It is a list of tuple with 2 args, 1st arg is the module name,
        2nd arg is the properties
        [
            ("my.modyule.name", {
                "db": "",
                "options": {
                    **kw
                }
            }),
            ()...
        ]

        It is a list of tuples to keep the order of the imports. If you
        require dependencies from other packages, dependencies must be placed
        before the calling package.


        To install 3rd party apps
        It is required that __init__ has a method called 'setup(**kw)'
        which will be used to setup the defaul app.



        INSTALLED_APPS = {
            "my.module.name": {
                "db": "",
                "options": {
                    **kw
                }
            }
        }

        To include additional modules, use `modules` keys contain the other module
        in a dict which also have `setup(**kw)`. The modules are relative to the
        current app path. and can contain the following kwargs:
                - route
                - nav
                - decorators

        *options will inherit from the package root, so place all options in there

            INSTALLED_APPS = {
                "my.module.name": {
                    "db": "",
                    "options": {
                        **kw
                    },
                    "modules": {
                        "module_a": {
                            "route": "/",
                            "nav": {

                            }
                        },
                        "module_b": {
                            "route": "/",
                            "decorators": []
                        }
                    }
                }
            }
        :return:
        """
        if "INSTALLED_APPS" in cls._app.config:
            _ = []

            def install_app(app, kwargs):
                print(app)
                _.append(import_string(app)(**kwargs))

            for a, prop in cls._app.config["INSTALLED_APPS"].items():
                modules = prop["modules"] if "modules" in prop else None
                _kwargs = {
                    "app": cls._app,
                    "db": import_string(prop.get("db")) if "db" in prop else None,
                    "route": prop.get("route") or "/",
                    "nav": prop.get("nav") or {"title": None},
                    "decorators": [import_string(d) for d in prop.get("decorators")]
                                    if "decorators" in prop
                                    else [],
                    "options": prop.get("options") or {}
                }

                install_app("%s.setup" % a, _kwargs)
                if modules:
                    if isinstance(modules, list):
                        for m in modules:
                            install_app("%s.%s.setup" % (a, m), _kwargs)
                    elif isinstance(modules, dict):
                        for n, kw in modules.items():
                            kw2 = {
                                "app": _kwargs["app"],
                                "db": _kwargs["db"],
                                "route": kw.get("route") or "/",
                                "nav": kw.get("nav") or {"title": None},
                                "decorators": [import_string(d) for d in kw.get("decorators")]
                                    if "decorators" in prop
                                    else [],
                                "options": _kwargs["options"]
                            }
                            install_app("%s.%s.setup" % (a, n), kw2)
            return _

    @classmethod
    def render(cls, data={}, _template=None, _layout=None, **kwargs):
        """
        To render data to the associate template file of the action view
        :param data: The context data to pass to the template
        :param _template: The file template to use. By default it will map the classname/action.html
        :param _layout: The body layout, must contain {% include __template__ %}
        """
        if not _template:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split(".")[-1]
            action_name = stack[3]      # The method being called in the class
            view_name = cls.__name__    # The name of the class without View

            if view_name.endswith("View"):
                view_name = view_name[:-4]
            _template = "%s/%s.html" % (view_name, action_name)

        data = data or dict()
        if kwargs:
            data.update(kwargs)
        data["__"] = cls._global
        data["__template__"] = _template

        return render_template(_layout or cls.base_layout, **data)

    @classmethod
    def g(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._global.update(kwargs)

    @classmethod
    def _add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = "%s/assets.yml" % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def _setup_logger(cls):

        logging_config = cls._app.config["LOGGING_CONFIG"] \
            if "LOGGING_CONFIG" in cls._app.config else None
        if not logging_config:
            logging_cls = cls._app.config["LOGGING_CLASS"] \
                if "LOGGING_CLASS" in cls._app.config else "logging.StreamHandler"
            logging_config = {
                "version": 1,
                "handlers": {
                    "default": {
                        "class": logging_cls
                    }
                },
                'loggers': {
                    '': {
                        'handlers': ['default'],
                        'level': 'WARN',
                    }
                }
            }

        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger("root")
        cls._app._logger = cls.logger
        cls._app._loger_name = cls.logger.name

    @classmethod
    def _register(cls, app, base_route=None, subdomain=None, route_prefix=None,
                 trailing_slash=None):
        """Registers a Magic class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param base_route: The base path to use for all routes registered for
                           this class. Overrides the base_route attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes base_route. Overrides
                             the class' route_prefix if it has been set.
        """

        if cls is Magic:
            raise TypeError("cls must be a subclass of Magic, not Magic itself")

        # Assign views
        setattr(views, cls.__name__, cls)

        if base_route:
            cls.orig_base_route = cls.base_route
            cls.base_route = base_route

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        for name, value in get_interesting_members(Magic, cls):
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy,
                                         subdomain=subdomain,
                                         **options)
                elif name in cls.__special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                        if name == "index":
                            if hasattr(value, "_methods_cache"):
                                methods = value._methods_cache
                    else:
                        methods = [name.upper()]

                    rule = cls.build_rule("/", value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip("/")
                    app.add_url_rule(rule, route_name, proxy,
                                     methods=methods,
                                     subdomain=subdomain)

                else:
                    methods = value._methods_cache \
                        if hasattr(value, "_methods_cache") \
                        else ["GET"]

                    name = utils.dasherize(name)
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy,
                                     subdomain=subdomain,
                                     methods=methods)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError("Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        if hasattr(cls, "orig_base_route"):
            cls.base_route = cls.orig_base_route
            del cls.orig_base_route

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash

    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the Magic subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)

            # You can also return a dict or None, it will pass it to render
            if isinstance(response, dict) or response is None:
                response = response or {}
                if hasattr(i, "_renderer"):
                    response = i._renderer(response)
                else:
                    df_v_t = "%s/%s.html" % (cls.__name__, view.__name__)
                    response.setdefault("_template", df_v_t)
                    response = i.render(**response)

            if not isinstance(response, Response):
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `base_route` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        base_route = cls.get_base_route()
        if base_route:
            rule_parts.append(base_route)

        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def get_base_route(cls):
        """Returns the route base to use for the current class."""

        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [r[2] for r in base_rule]
        else:
            if cls.__name__.endswith("View"):
                base_route = cls.__name__[:-4].lower()
            else:
                base_route = cls.__name__.lower()

        return base_route.strip("/")

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":%s" % method_name

    @staticmethod
    def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
        # Put the rule cache on the method itself instead of globally
        if rule is None:
            rule = utils.dasherize(f.__name__) + "/"
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, kwargs)]}
        elif not f.__name__ in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, kwargs)]
        else:
            # when and endpoint accepts multiple METHODS, ie: post(), get()
            if append_method:
                for r in f._rule_cache[f.__name__]:
                    if r[0] == rule and "methods" in r[1] and "methods" in kwargs:
                        r[1]["methods"] = list(set(r[1]["methods"] + kwargs["methods"]))
            else:
                f._rule_cache[f.__name__].append((rule, kwargs))
        return f


# MagicWand
MagicWand = Magic()

# ------------------------------------------------------------------------------


def get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members
            if not member[0] in base_members
            and ((hasattr(member[1], "__self__") and not member[1].__self__ in inspect.getmro(cls)) if _py2 else True)
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_"))


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
            and not inspect.ismethod(inner_method):
            continue
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec


class DecoratorCompatibilityError(Exception):
    pass


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class MagicError(Exception):
    pass
