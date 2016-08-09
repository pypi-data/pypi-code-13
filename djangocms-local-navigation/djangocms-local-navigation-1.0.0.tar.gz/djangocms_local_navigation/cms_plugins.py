from bs4 import BeautifulSoup

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.templatetags.cms_tags import get_placeholder_content

from .conf import settings


class LocalNavigationPlugin(CMSPluginBase):
    module = "Local navigation"
    name = "Local menu"
    render_template = "djangocms_local_navigation/menu.html"

    def render(self, context, instance, placeholder):
        # Set a flag in the context to avoid recursion, since we'll be
        # rendering the placeholder in which this plugin is
        if context.get('_local_navigation_rendering', False):
            return context
        else:
            context['_local_navigation_rendering'] = True

        placeholder_text = get_placeholder_content(
            context, context['request'], context['current_page'], placeholder,
            inherit=False, default=''
        )
        placeholder_soup = BeautifulSoup(placeholder_text, settings.XML_PARSER)
        headings = placeholder_soup.find_all(settings.NAV_ELEMENTS)

        menu_items = [
            (heading.text, '#' + heading['id'])
            for heading in headings
            if 'id' in heading.attrs
        ]
        context['local_menu_items'] = menu_items

        return context

plugin_pool.register_plugin(LocalNavigationPlugin)
