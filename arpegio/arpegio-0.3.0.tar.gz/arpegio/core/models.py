"""Arpegio's models."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.db import models


@python_2_unicode_compatible
class ContentMixin(models.Model):
    """
    This model contains three fields: title, slug and content.
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title or '(No title)'

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        elif not self.slug:
            raise ValueError('You have to give this object a slug.')
        super(ContentMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Timestampable(models.Model):  # pylint: disable=model-missing-unicode
    """
    This model adds a creation and modification date fields.
    """
    creation_date = models.DateTimeField(blank=True, default=now)
    modification_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.modification_date = now()
        super(Timestampable, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Sluggable(models.Model):  # pylint: disable=model-missing-unicode
    """
    This models adds a title and slug fields. The slug is derived from the
    title field.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, editable=False)

    def save(self, *args, **kwargs):
        self.slug = self.name
        super(Sluggable, self).save(*args, **kwargs)

    class Meta:
        abstract = True
