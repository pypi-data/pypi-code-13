# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
)


class TestClassesValidity(object):
    def test_categories_model_integrity(self):
        from tests.testproject.models import Category

        assert hasattr(Category, 'article_set')
        assert hasattr(Category, 'entry_set')

        assert isinstance(Category.article_set, ManyToManyDescriptor)
        assert isinstance(Category.entry_set, ManyToManyDescriptor)

    def test_through_model_module_presence(self):
        import tests.testproject.models as test_models

        assert hasattr(test_models, 'ArticleCategory')
        assert hasattr(test_models, 'EntryCategory')
        assert hasattr(test_models, 'ItemCategory')

    def test_through_model_module_identity(self):
        from tests.testproject.models import (
            ArticleCategory,
            ItemCategory,
            EntryCategory,
        )

        expected_module_name = 'tests.testproject.models'

        assert ArticleCategory.__module__ == expected_module_name
        assert EntryCategory.__module__ == expected_module_name
        assert ItemCategory.__module__ == expected_module_name

    def test_articlecategory_model_integrity(self):
        from tests.testproject.models import ArticleCategory

        assert ArticleCategory._meta.abstract is False

        assert hasattr(ArticleCategory, 'article')
        assert isinstance(ArticleCategory.article, ForwardManyToOneDescriptor)

        assert hasattr(ArticleCategory, 'category')
        assert isinstance(ArticleCategory.category, ForwardManyToOneDescriptor)

    def test_entrycategory_model_integrity(self):
        from tests.testproject.models import EntryCategory

        assert EntryCategory._meta.abstract is False

        assert hasattr(EntryCategory, 'entry')
        assert isinstance(EntryCategory.entry, ForwardManyToOneDescriptor)

        assert hasattr(EntryCategory, 'category')
        assert isinstance(EntryCategory.category, ForwardManyToOneDescriptor)


class TestQuerySets(object):
    def test_articlecategory_querying(self, articles):
        from tests.testproject.models import ArticleCategory

        for article in articles.prefetch_related('categories').all():
            assert ArticleCategory.objects.filter(
                article__name=article.name,
                category__name__in=[c.name for c in article.categories.all()],
            ).count() == article.categories.count()

    def test_entrycategory_querying(self, entries):
        from tests.testproject.models import EntryCategory

        for entry in entries.prefetch_related('categories').all():
            assert EntryCategory.objects.filter(
                entry__name=entry.name,
                category__name__in=[c.name for c in entry.categories.all()],
            ).count() == entry.categories.count()
