# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from cms.models import CMSPlugin


@python_2_unicode_compatible
class Markdown(CMSPlugin):
    body = models.TextField()

    def __str__(self):
        return self.body[:64]