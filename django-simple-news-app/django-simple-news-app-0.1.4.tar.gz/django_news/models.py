# coding=utf-8
from __future__ import absolute_import, unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_('User'))
    name = models.CharField(_('Displayed name'), max_length=300)
    photo = models.ImageField(_('Photo'), blank=True, null=True)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return '{} ({})'.format(self.name, self.user)

    @classmethod
    def is_author(cls, user):
        try:
            return cls.objects.filter(user=user).exists()
        except cls.DoesNotExist:
            return False


class CategoryManager(models.Manager):
    def get_active(self):
        return self.filter(entries__active=True,
                           entries__date__lte=now()).distinct()


@python_2_unicode_compatible
class Category(models.Model):
    WEIGHT_CHOICES = tuple((i, i) for i in range(-10, 10))

    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    weight = models.IntegerField(
        _('Weight'), choices=WEIGHT_CHOICES, default=0,
        help_text=_('Weight controls order of categories in menus')
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-weight', 'id')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('django_news:entry_list', kwargs={'slug': self.slug})

    @cached_property
    def updated(self):
        return self.entries.get_active().aggregate(Max('updated')).get(
            'updated__max', now()
        )


class EntryManager(models.Manager):
    def get_all(self):
        return self.all().order_by('-date').select_related()

    def get_active(self, slug=None):
        qs = self.get_all().filter(active=True, date__lte=now())
        if slug is not None:
            qs = qs.filter(category__slug=slug)

        return qs


@python_2_unicode_compatible
class Entry(models.Model):
    author = models.ForeignKey(Author, verbose_name=_('Author'),
                               related_name='entries')
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 related_name='entries')

    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'))
    subtitle = models.CharField(_('Subtitle'), max_length=400, blank=True)
    abstract = models.CharField(_('Abstract'), max_length=1000, blank=True)
    text = RichTextUploadingField(_('Text'))

    active = models.BooleanField(
        verbose_name=_('Active'), default=True,
        help_text=_('Show entry in news feed')
    )
    date = models.DateTimeField(
        verbose_name=_('Date'), null=False,
        help_text=_('Show entry only starting from this date')
    )

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    objects = EntryManager()

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        unique_together = ('category', 'slug')

    def __str__(self):
        return '{}/{}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return reverse('django_news:entry_detail',
                       kwargs={'slug': self.slug,
                               'category_slug': self.category.slug})
