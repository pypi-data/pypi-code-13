# -*- coding:utf-8 -*-
"""
# Following code is a tweak for this way of defining custom through models:

# ----- Category models -----
class Category(models.Model):
    name = models.CharField(max_length=255)


# ----- Abstract models -----
class AbstractItem(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


# ----- Article models -----
class Article(AbstractItem):
    categories = models.ManyToManyField(Category, through='ArticleCategory')


class ArticleCategory(models.Model):
    article = models.ForeignKey(Article)
    category = models.ForeignKey(Category)


# ----- Entry models -----
class Entry(AbstractItem):
    categories = models.ManyToManyField(Category, through='EntryCategory')


class EntryCategory(models.Model):
    entry = models.ForeignKey(Entry)
    category = models.ForeignKey(Category)
"""
from __future__ import absolute_import, unicode_literals

from django.db import models

from abstract_relations.models import AbstractManyToManyField


# ----- Category models -----
class Category(models.Model):
    name = models.CharField(max_length=255)


# ----- Abstract models -----
class ItemCategory(models.Model):
    category = models.ForeignKey(Category)

    class Meta:
        abstract = True


class AbstractItem(models.Model):
    name = models.CharField(max_length=255)
    categories = AbstractManyToManyField(Category, through=ItemCategory)

    class Meta:
        abstract = True


# ----- Article models -----
class Article(AbstractItem):
    pass


# ----- Entry models -----
class Entry(AbstractItem):
    pass
