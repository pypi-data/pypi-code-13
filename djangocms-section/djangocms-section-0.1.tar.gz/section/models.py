# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from .conf import settings

@python_2_unicode_compatible
class Section(CMSPlugin):
    STYLE_CHOICES = settings.SECTION_STYLE_CHOICES
    DEFAULT_STYLE = settings.SECTION_DEFAULT_STYLE

    headline = models.CharField(max_length=512, verbose_name=_('headline'), blank=True)
    image = FilerImageField(verbose_name=_('image'), related_name='section')
    image_caption = models.CharField(max_length=512, verbose_name=_('image caption'), blank=True)
    style = models.CharField(verbose_name=_('style'), choices=STYLE_CHOICES, default=DEFAULT_STYLE, max_length=50,
        blank=False)

    def __str__(self):
        if self.headline:
            return self.headline
        else:
            return self.id
