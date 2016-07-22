# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils.encoding import python_2_unicode_compatible

from cms.api import add_plugin
from cms.models import Placeholder

from djangocms_text_ckeditor.cms_plugins import TextPlugin
from filer.tests.models import FilerApiTests

from section.cms_plugins import SectionPlugin
from section.conf import settings
from section.models import Section

class SectionTests(TestCase):
    HEADLINE = 'Test headline'
    IMAGE_CAPTION = 'Test image caption'

    def get_filer_image(self):
        if not getattr(self, 'image', None):
            filer_test = FilerApiTests()
            self.image = filer_test.create_filer_image()
        return self.image

    def get_model_instance(self, data={}):
        data.setdefault('headline', self.HEADLINE)
        data.setdefault('image', self.get_filer_image())
        data.setdefault('image_caption', self.IMAGE_CAPTION)
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            SectionPlugin,
            'en',
            **data
        )
        return model_instance

    def test_create_plugin(self):
        """
        Test creating a Section plugin
        """
        model_instance = self.get_model_instance()
        plugin_instance = model_instance.get_plugin_class_instance()
        self.assertTrue(isinstance(model_instance, Section))
        self.assertTrue(isinstance(plugin_instance, SectionPlugin))

    def test_plugin_rendering(self):
        """
        Test that context is populated properly.
        """
        model_instance = self.get_model_instance()
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertEqual(context['headline'], self.HEADLINE)
        self.assertEqual(context['image'], self.get_filer_image())
        self.assertEqual(context['image_caption'], self.IMAGE_CAPTION)
        self.assertEqual(context['style'], settings.SECTION_DEFAULT_STYLE)

    def test_text_plugin_creation(self):
        """
        Test if a child Text plugin is created on save, given that there's none yet.
        """
        model_instance = self.get_model_instance()
        # test if children exist
        self.assertTrue(model_instance.get_children())
        self.assertTrue(isinstance(model_instance.get_children()[0], TextPlugin))
