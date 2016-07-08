import os
import settings

from jinja2 import Environment, FileSystemLoader

from werkzeug.wrappers import Response



class View(object):

    @property
    def authorized_method(self):
        authorized_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

        return [method for method in authorized_methods if hasattr(self, method.lower())]

    def as_view(self, request, *args, **kwargs):
        template_path = os.path.join(os.path.dirname("."), settings.TEMPLATE_DIR)
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True)
        return self.dispatch(request, *args, **kwargs)

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch(self, request, *args, **kwargs):
        if request.method in self.authorized_method:
            return getattr(self, request.method.lower())(request, *args, **kwargs)
