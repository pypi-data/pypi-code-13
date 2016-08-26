# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest


@pytest.fixture
def categories(db):
    from tests.testproject.models import Category

    for i in range(1, 10):
        Category.objects.create(name='category_%s' % i)

    return Category.objects.all()


@pytest.fixture
def articles(categories, db):
    from tests.testproject.models import Article, ArticleCategory

    for i, category in enumerate(categories, start=1):
        article = Article.objects.create(name='article_%s' % i)
        ArticleCategory.objects.create(article=article, category=category)

    return Article.objects.all()


@pytest.fixture
def entries(categories, db):
    from tests.testproject.models import Entry, EntryCategory

    for i, category in enumerate(categories, start=1):
        entry = Entry.objects.create(name='entry_%s' % i)
        EntryCategory.objects.create(entry=entry, category=category)

    return Entry.objects.all()
