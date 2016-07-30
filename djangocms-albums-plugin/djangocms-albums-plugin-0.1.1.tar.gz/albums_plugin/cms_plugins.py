from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from albums_plugin.models import AlbumsPlugin
from django.utils.translation import ugettext as _


class CMSAlbumsPlugin(CMSPluginBase):
    model = AlbumsPlugin
    module = _('Albums')
    render_template = 'albums_plugin/albums_plugin.html'

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CMSAlbumsPlugin)
