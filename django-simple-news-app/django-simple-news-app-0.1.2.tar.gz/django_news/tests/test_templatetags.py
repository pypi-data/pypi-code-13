# coding=utf-8
from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from ..models import Author, Category, Entry
from ..templatetags.django_news import get_active_categories


class GetAllCategoriesTestCase(TestCase):
    def test_no_categories(self):
        """Test that template tag returns an empty queryset when no categories
        present
        """
        categories = get_active_categories({})
        self.assertFalse(categories)

    def test_no_active_categories(self):
        """Test that template tag returns an empty queryset when all categories
        are empty or contain only inactive entries
        """
        user = User.objects.create(username='test')
        author = Author.objects.create(user=user, name='author')
        c1 = Category.objects.create(name='c1', slug='c1')
        Category.objects.create(name='c2', slug='c2')
        Entry.objects.create(category=c1, author=author, title='e1', text='e1',
                             slug='e1',
                             date=now() - timedelta(days=1), active=False)
        Entry.objects.create(category=c1, author=author, title='e1', text='e1',
                             slug='e2',
                             date=now() + timedelta(days=1), active=True)

        categories = get_active_categories({})
        self.assertFalse(categories)

    def test_has_active_categories(self):
        """Test that template tag returns an only categories that contain
        at least one active entry
        """
        user = User.objects.create(username='test')
        author = Author.objects.create(user=user, name='author')
        c1 = Category.objects.create(name='c1', slug='c1')
        c2 = Category.objects.create(name='c2', slug='c2')
        c3 = Category.objects.create(name='c3', slug='c3')
        Category.objects.create(name='c4', slug='c4')
        Entry.objects.create(category=c1, author=author, title='e1', text='e1',
                             slug='e1',
                             date=now() - timedelta(days=1), active=False)
        Entry.objects.create(category=c1, author=author, title='e1', text='e1',
                             slug='e2',
                             date=now() + timedelta(days=1), active=True)
        Entry.objects.create(category=c2, author=author, title='e1', text='e1',
                             slug='e3',
                             date=now() - timedelta(days=1), active=True)
        Entry.objects.create(category=c3, author=author, title='e1', text='e1',
                             slug='e4',
                             date=now() - timedelta(days=2), active=True)
        Entry.objects.create(category=c3, author=author, title='e1', text='e1',
                             slug='e5',
                             date=now() - timedelta(days=2), active=False)

        categories = get_active_categories({})
        self.assertEqual(len(categories), 2)
        self.assertIn(c2, categories)
        self.assertIn(c3, categories)

    def test_context_is_used(self):
        """Test that template tag doesn't hit database and uses context if it
        contains a list of categories
        """
        c1 = Category.objects.create(name='c1', slug='c1')
        c2 = Category.objects.create(name='c2', slug='c2')
        category_list = [c1, c2]

        categories = get_active_categories({'category_list': category_list})
        self.assertIs(category_list, categories)

    def test_context_is_not_used_without_categories_inside(self):
        """Test that template tag hits database and don't uses context if it
        contains a list of objects other than Category instances
        """
        category_list = ['c1', 'c2']

        categories = get_active_categories({'category_list': category_list})
        self.assertNotEqual(category_list, categories)
        self.assertFalse(categories)
