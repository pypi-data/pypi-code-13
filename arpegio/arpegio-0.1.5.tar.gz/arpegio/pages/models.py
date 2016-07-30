"""Pages models."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


@python_2_unicode_compatible
class Page(models.Model):
    """Page model."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               )
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    content = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, default=now)
    modified_date = models.DateTimeField(editable=False)

    def get_absolute_url(self):
        """Get the absolute url of a page"""
        return reverse('pages:page', kwargs={'slug': self.slug})

    def __str__(self):
        """String representation of Page object"""
        return self.title or 'No title'

    def save(self, *args, **kwargs):
        """Save the Page object and create a slug"""
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        elif self.slug:
            self.slug = self.slug
        else:
            assert ValueError
        self.modified_date = now()
        super(Page, self).save(*args, **kwargs)
