# coding=utf-8
from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from ..models import Author, Category, Entry


class CategoryManagerTestCase(TestCase):
    def test_no_categories(self):
        """Test that manager returns an empty queryset when no categories
        present
        """
        categories = Category.objects.get_active()
        self.assertFalse(categories)

    def test_no_active_categories(self):
        """Test that manager returns an empty queryset when all categories
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

        categories = Category.objects.get_active()
        self.assertFalse(categories)

    def test_has_active_categories(self):
        """Test that manager returns an only categories that contain
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
        Entry.objects.create(category=c2, author=author, title='e1', text='e1',
                             slug='e33',
                             date=now() - timedelta(days=1), active=True)
        Entry.objects.create(category=c3, author=author, title='e1', text='e1',
                             slug='e4',
                             date=now() - timedelta(days=2), active=True)
        Entry.objects.create(category=c3, author=author, title='e1', text='e1',
                             slug='e5',
                             date=now() - timedelta(days=2), active=False)

        categories = Category.objects.get_active()
        self.assertEqual(len(categories), 2)
        self.assertIn(c2, categories)
        self.assertIn(c3, categories)


class EntryManagerTestCase(TestCase):
    def test_no_entries(self):
        """Test that manager returns an empty queryset when no entries
        present
        """
        entries = Entry.objects.get_active()
        self.assertFalse(entries)

    def test_has_active_entries(self):
        """Test that manager returns only active entries"""
        user = User.objects.create(username='test')
        author = Author.objects.create(user=user, name='author')
        c1 = Category.objects.create(name='c1', slug='c1')
        c2 = Category.objects.create(name='c2', slug='c2')
        Category.objects.create(name='c3', slug='c3')
        Entry.objects.create(category=c1, author=author, title='e1',
                             text='e1', slug='e1',
                             date=now() - timedelta(days=1), active=False)
        Entry.objects.create(category=c1, author=author, title='e1',
                             text='e1', slug='e2',
                             date=now() + timedelta(days=1), active=True)
        e3 = Entry.objects.create(category=c1, author=author, title='e1',
                                  text='e1', slug='e3',
                                  date=now() - timedelta(days=1), active=True)
        e4 = Entry.objects.create(category=c2, author=author, title='e1',
                                  text='e1', slug='e4',
                                  date=now() - timedelta(days=2), active=True)
        Entry.objects.create(category=c2, author=author, title='e1',
                             text='e1', slug='e5',
                             date=now() - timedelta(days=2), active=False)

        entries = Entry.objects.get_active()
        self.assertEqual(len(entries), 2)
        self.assertIn(e3, entries)
        self.assertIn(e4, entries)

    def test_category_has_active_entries(self):
        """Test that manager returns only active entries from certain category
        """
        user = User.objects.create(username='test')
        author = Author.objects.create(user=user, name='author')
        c1 = Category.objects.create(name='c1', slug='c1')
        c2 = Category.objects.create(name='c2', slug='c2')
        Category.objects.create(name='c3', slug='c3')
        Entry.objects.create(category=c1, author=author, title='e1',
                             text='e1', slug='e1',
                             date=now() - timedelta(days=1), active=False)
        Entry.objects.create(category=c1, author=author, title='e1',
                             text='e1', slug='e2',
                             date=now() + timedelta(days=1), active=True)
        e3 = Entry.objects.create(category=c1, author=author, title='e1',
                                  text='e1', slug='e3',
                                  date=now() - timedelta(days=1), active=True)
        Entry.objects.create(category=c2, author=author, title='e1',
                             text='e1', slug='e4',
                             date=now() - timedelta(days=2), active=True)
        Entry.objects.create(category=c2, author=author, title='e1',
                             text='e1', slug='e5',
                             date=now() - timedelta(days=2), active=False)

        entries = Entry.objects.get_active('c1')
        self.assertEqual(len(entries), 1)
        self.assertIn(e3, entries)
