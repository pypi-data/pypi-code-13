# -*- coding: utf-8 -*-
"""Implementation of CMSPluginBase class for ``cmsplugin-markdown``."""
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_markdown.models import Markdown


class MarkdownPlugin(CMSPluginBase):
    model = Markdown
    name = _('Markdown')
    render_template = 'djangocms_markdown/markdown.html'
    change_form_template = 'djangocms_markdown/change_form.html'

    def render(self, context, instance, placeholder):
        super(MarkdownPlugin, self).render(context, instance, placeholder)

        context['text'] = instance.body
        return context


plugin_pool.register_plugin(MarkdownPlugin)
