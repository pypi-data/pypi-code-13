"""Models for the tags app."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from arpegio.core.models import Sluggable


@python_2_unicode_compatible
class Tag(Sluggable, models.Model):
    """Tag model."""

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Taggable(models.Model):
    """This model adds a tags m2m field."""

    tags = models.ManyToManyField(Tag)

    class Meta:
        abstract = True
