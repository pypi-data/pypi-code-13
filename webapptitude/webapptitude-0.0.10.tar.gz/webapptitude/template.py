
# TODO: standard Jinja filters & globals

import math
import webapp2
import os
import util  # webapptitude's "util"

from webapp2_extras import i18n
from webapp2_extras import jinja2

try:
    from google.appengine.api import users
except ImportError:
    users = None


def humanize(number):
    """
    Convert numbers to human abbreviations, example:
         1000 -> 1K
         1000000 -> 1M
         1000000000 -> 1B

    """
    log = math.floor(math.log10(number))
    log = int(log - (log % 3))
    result = number / math.pow(10, log)
    suffix = {0: '', 3: 'K', 6: 'M', 9: 'B'}
    return ('%d%s' % (result, suffix[log]))



def _filters(filterdict):
    # filterdict['yaml_bootstrap_navigation'] = yaml_bootstrap_navigation
    filterdict['repr'] = repr
    filterdict['str'] = str
    filterdict['humanize'] = humanize
    return filterdict


def _globals(globaldict):
    globaldict['is_dev_server'] = util.is_dev_server()
    return globaldict


class RequestHandler(webapp2.RequestHandler):


    @property
    def template_filters(self):
        """A generator of additional filters to register."""
        raise NotImplementedError

    @property
    def template_globals(self):
        """A generator of additional globals to register."""
        raise NotImplementedError

    @property
    def locale(self):
        header = self.request.headers.get('Accept-Language', 'en_US')
        locales_req = [ i.split(';')[0] for i in header.split(',') ]
        return locales_req

    @webapp2.cached_property
    def jinja2_environment(self):
        """Prepare the Jinja2 template environment configuration."""
        template_path = os.environ.get('TEMPLATE_PATH', 'templates')
        extensions = ['autoescape', 'i18n', 'do', 'loopcontrols', 'with_']

        i18n.get_i18n().set_locale(self.locale[0])

        env_filters = {}
        env_globals = ({
            'url_for': self.uri_for,
            'uri_for': self.uri_for,
            'user': (users and users.get_current_user()),
            'logout_url': (users and users.create_logout_url),
            'login_url': (users and users.create_login_url),
            'request': self.request,
            'request_path': self.request.path,
            'request_query': self.request.input,
            'environ': os.environ,
            'page': {}
        })

        try:
            for key, function in self.template_filters:
                env_filters[key] = function
        except NotImplementedError:
            pass

        try:
            for key, value in self.template_globals:
                env_globals[key] = value
        except NotImplementedError:
            pass

        # Inherit standard module
        env_filters = _filters(env_filters)
        env_globals = _globals(env_globals)

        return {
            'template_path': getattr(self, 'template_path', template_path),
            'environment_args': {
                'autoescape': True,
                'extensions': ["jinja2.ext.%s" % (i,) for i in extensions]
            },
            'filters': env_filters,
            'globals': env_globals
        }

    @webapp2.cached_property
    def jinja2(self):
        """Prepare the template engine instance."""
        return jinja2.Jinja2(app=self.app, config=self.jinja2_environment)

    def render_to_response(self, *args, **kwargs):
        """Simple compatibility functionf or DJango's style."""
        return self.respond_with_template(*args, **kwargs)

    def respond_with_template(self, template_path, values=None,
                              content_type=None, **context):
        if values is None:
            values = context
        elif isinstance(values, dict):
            values.update(context)
        if isinstance(content_type, basestring):
            self.response.headers['Content-Type'] = content_type

        result = self.jinja2.render_template(template_path, **values)
        return self.response.write(result)


def TemplatePartial(template_path, chunk_name=None, base_class=RequestHandler):
    """
    Prepare a request handler from an embedded macro in a template.

    This regards {chunk_name} as referring to a macro defined in a template.

    Example macro in <templates/markdown.html>:

        {% macro content(markdown_text) %}
            {{ mardown_text|markdownify|safe }}
        {% endmacro %}


    The request handler can then be added to an application:

        partial = TemplatePartial('markdown.html', /content')
        app.router.add(webapp2.Route('/', partial))

    """
    class _partial(base_class):

        def get_partial(self, *args, **kwargs):
            _jinja2 = self.jinja2
            _part = _jinja2.get_template_attribute(
                template_path,
                chunk_name
            )
            return _part(*args, **kwargs)

        def get(self, *args, **kwargs):
            content = self.get_partial(*args, **kwargs)
            self.response.write(content)

    return _partial


