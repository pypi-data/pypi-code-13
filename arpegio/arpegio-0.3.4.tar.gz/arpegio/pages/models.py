"""Pages models."""
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models

from arpegio.core.models import ContentMixin, Timestampable


class Page(ContentMixin,  # pylint:disable=model-missing-unicode
           Timestampable,
           models.Model):
    """Page model."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               )

    def get_absolute_url(self):
        """Get the absolute url of a page"""
        return reverse('pages:page', kwargs={'slug': self.slug})
