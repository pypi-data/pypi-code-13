"""Blog models."""
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models

from arpegio.core.models import ContentMixin, Timestampable
from .managers import PostManager


class Post(ContentMixin,  # pylint: disable=model-missing-unicode
           Timestampable,
           models.Model):
    """Post Model."""

    STATUS_CHOICES = (('D', 'Draft'),
                      ('PB', 'Public'),
                      ('PV', 'Private'),
                      ('T', 'Trash'),
                      )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE
                               )
    excerpt = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='post_covers',
                                       blank=True,
                                       null=True
                                       )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    sticky = models.BooleanField(default=False)

    objects = PostManager()

    def get_absolute_url(self):
        """Get the absolute url of a post"""
        return reverse('blog:post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-creation_date']
