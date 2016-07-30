"""Blog models."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from .managers import PostManager


@python_2_unicode_compatible
class Post(models.Model):
    """Post Model."""

    STATUS_CHOICES = (('D', 'Draft'),
                      ('PB', 'Public'),
                      ('PV', 'Private'),
                      ('T', 'Trash'),
                      )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE
                               )
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    content = models.TextField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='post_covers',
                                       blank=True,
                                       null=True
                                       )
    creation_date = models.DateTimeField(blank=True, default=now)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    sticky = models.BooleanField(default=False)
    modified_date = models.DateTimeField(editable=False)

    objects = PostManager()

    def get_absolute_url(self):
        """Get the absolute url of a post"""
        return reverse('blog:post', kwargs={'slug': self.slug})

    def __str__(self):
        """String representation of Post object"""
        return self.title or 'No title'

    def save(self, *args, **kwargs):
        """Save the Post object and create a slug"""
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        elif self.slug:
            self.slug = self.slug
        else:
            assert ValueError
        self.modified_date = now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-creation_date']
