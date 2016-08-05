"""Models for the categories app."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from arpegio.core.models import Sluggable


@python_2_unicode_compatible
class Category(Sluggable, models.Model):
    """Category model."""

    parent = models.ForeignKey('self', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Categorizable(models.Model):
    """This model adds a category m2m field."""

    categories = models.ManyToManyField(Category)

    class Meta:
        abstract = True
