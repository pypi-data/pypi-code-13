
from django.db import models


class SeoMeow(models.Model):

    url = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    keywords = models.TextField(blank=True, default='')
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    class Meta:
        db_table = 'seomeow'
        ordering = ('url', 'pk')
        verbose_name = 'seo-meow tags'
        verbose_name_plural = 'seo-meow'
