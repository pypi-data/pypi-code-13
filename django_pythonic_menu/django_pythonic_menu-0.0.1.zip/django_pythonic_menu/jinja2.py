from jinja2 import nodes
from jinja2.ext import Extension


class RenderMenuExtension(Extension):
    """
    used as {% render_menu 'menu.ClassName' as menu %}
    """
    tags = {'render_menu'}

    def parse(self, parser):
        render_menu = next(parser.stream)

        return nodes.Assign()

