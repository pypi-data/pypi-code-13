# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Category, Entry


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        return self.model.objects.get_active()


class EntryListView(ListView):
    """A view that shows a list of active entries of certain category.

    If there are no active entries in category, request results in 404 error.

    Entry is called active only if `active` flag is set to ``True`` and
    publication date is in past.
    """
    model = Entry
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.get_active(self.kwargs['slug']).defer('text')

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        if not len(context['object_list']):
            raise Http404

        context['category'] = context['object_list'][0].category
        return context


class EntryDetailView(DetailView):
    """A view that shows an entry of certain category.

    If entry is inactive, request results in 404 error.

    Entry is called active only if `active` flag is set to ``True`` and
    publication date is in past.
    """
    model = Entry

    def get_queryset(self):
        return self.model.objects.get_active(self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['category'] = context['object'].category
        return context
