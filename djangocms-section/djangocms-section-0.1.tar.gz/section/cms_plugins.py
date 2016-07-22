# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .models import Section

class SectionPlugin(CMSPluginBase):
    model = Section
    name = _('Section')
    TEMPLATE_NAME = "section/%s.html"
    render_template = TEMPLATE_NAME % 'default'
    allow_children = True
    child_classes = settings.SECTION_CHILD_PLUGINS

    def save_model(self, request, obj, form, change):
        value = super(SectionPlugin, self).save_model(request, obj, form, change)
        if not obj.get_children():
            try:
                from cms.api import add_plugin
                from djangocms_text_ckeditor.cms_plugins import TextPlugin
                add_plugin(self.placeholder, TextPlugin, self.cms_plugin_instance.language,
                    target=self.cms_plugin_instance, body=settings.SECTION_DEFAULT_TEXT)
            except ImportError:
                pass
        return value

    def render(self, context, instance, placeholder):
        self.render_template = select_template((
            self.TEMPLATE_NAME % instance.style,
            self.render_template)
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(SectionPlugin)
