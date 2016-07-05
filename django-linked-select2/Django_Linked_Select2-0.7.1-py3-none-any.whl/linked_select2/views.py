# -*- coding: utf-8 -*-
"""JSONResponse views for model widgets."""
from __future__ import absolute_import, unicode_literals

from django.core import signing
from django.core.signing import BadSignature
from django.http import Http404, JsonResponse
from django.views.generic.list import BaseListView

from django_select2.cache import cache
from django_select2.conf import settings

from linked_select2.forms import LinkedModelSelect2Mixin


class LinkedAutoResponseView(BaseListView):
    """
    View that handles requests from heavy model widgets and
    their linked versions.

    The view only supports HTTP's GET method.
    """
    link_query_prefix = None

    def get_linked_widget_classes(self):
        return (
            LinkedModelSelect2Mixin,
        )

    def get(self, request, *args, **kwargs):
        """
        Return a :class:`.django.http.JsonResponse`.

        Example::

            {
                'results': [
                    {
                        'text': "foo",
                        'id': 123
                    }
                ],
                'more': true
            }

        """
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return JsonResponse({
            'results': [
                {
                    'text': self.widget.label_from_instance(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
            ],
            'more': context['page_obj'].has_next()
        })

    def get_queryset(self):
        """
        Get QuerySet from cached widget.

        Django-Linked-Select2 querysets are reevaluated every time.
        """
        if isinstance(self.widget, self.get_linked_widget_classes()):
            return self.widget.filter_queryset(
                self.term,
                self.queryset,
                self.get_linked_fields()
            )
        return self.widget.filter_queryset(
            self.term,
            self.queryset,
        )

    def get_paginate_by(self, queryset):
        """Paginate response by size of widget's `max_results` parameter."""
        return self.widget.max_results

    def get_widget_or_404(self):
        """
        Get and return widget from cache.

        Raises:
            Http404: If if the widget can not be found or no id is provided.

        Returns:
            LinkedModelSelect2Mixin or ModelSelect2Mixin: Widget from cache.

        """
        field_id = self.kwargs.get(
            'field_id',
            self.request.GET.get('field_id', None)
        )

        if not field_id:
            raise Http404('No "field_id" provided.')

        try:
            key = signing.loads(field_id)
        except BadSignature:
            raise Http404('Invalid "field_id".')
        else:
            cache_key = '%s%s' % (settings.SELECT2_CACHE_PREFIX, key)
            widget_dict = cache.get(cache_key)
            if widget_dict is None:
                raise Http404('"field_id" not found')
            if widget_dict.pop('url') != self.request.path:
                raise Http404('"field_id" was issued for the view.')

        widget_cls = widget_dict.pop('cls')

        # Support both linked and nonlinked widgets
        if issubclass(widget_cls, self.get_linked_widget_classes()):
            self.queryset = qs = None
        else:
            qs, qs.query = widget_dict.pop('queryset')
            self.queryset = qs.all()

        widget_dict['queryset'] = self.queryset
        return widget_cls(**widget_dict)

    def get_linked_fields(self):
        """
        Extracts linked field values as query parameters from GET data.

        Returns:
            dict: Map of linked keys and their values.

        """
        link_query_prefix = getattr(
            settings, 'SELECT2_LINK_QUERY_PREFIX', 'link_')
        return {
            k[len(link_query_prefix):]: v
            for k, v in self.request.GET.items()
            if k.startswith(link_query_prefix)
        }
