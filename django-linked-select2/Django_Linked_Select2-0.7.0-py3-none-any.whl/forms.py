# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import reduce
from itertools import chain

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.utils.encoding import force_text

from django_select2.forms import (
    HeavySelect2Widget, HeavySelect2MultipleWidget, HeavySelect2TagWidget,
)


class LinkedModelSelect2Mixin(object):
    """
    Widget mixin that provides attributes and methods for
    :class:`.LinkedAutoResponseView`.
    """
    form = None
    """
    Form used to validate linked data. Names of fields in this form
    are used in the frontend.

    """
    model = None
    """
    Model of returned QuerySet. Can be `None` in class definition if
    :func:`LinkedModelSelect2Mixin.get_queryset` is properly overriden.

    """
    queryset = None
    search_fields = []
    """
    Model lookups that are used to filter the QuerySet.

    Example::

        search_fields = [
                'title__icontains',
            ]

    """

    max_results = 25
    """Maximal results returned by :class:`.LinkedAutoResponseView`."""

    def __init__(self, *args, **kwargs):
        """
        Overwrite class parameters if passed as keyword arguments.

        Args:
            model (django.db.models.Model): Model to select choices from.
            queryset (django.db.models.QuerySet): QuerySet to select
            choices from.
            search_fields (list): List of model lookup strings.
            max_results (int): Max. JsonResponse view page size.
            form (django.forms.Form): Form used to validate linked data.

        """
        self.model = kwargs.pop('model', self.model)
        self.queryset = kwargs.pop('queryset', self.queryset)
        self.search_fields = kwargs.pop('search_fields', self.search_fields)
        self.max_results = kwargs.pop('max_results', self.max_results)
        self.form = kwargs.pop('form', self.form)
        defaults = {'data_view': 'django_select2-json'}
        defaults.update(kwargs)
        super(LinkedModelSelect2Mixin, self).__init__(*args, **defaults)

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Add Django-Linked-Select2 specific data attributes."""
        attrs = super(LinkedModelSelect2Mixin, self).build_attrs(
            extra_attrs=extra_attrs, **kwargs)

        attrs['class'] += ' django-select2-linked'

        attrs.setdefault(
            'data-ajax--linked-fields',
            ' '.join(self.get_linked_fields())
        )
        attrs.setdefault(
            'data-ajax--link-query-prefix',
            getattr(settings, 'SELECT2_LINK_QUERY_PREFIX', 'link_')
        )
        attrs.setdefault(
            'data-ajax--linked-field-prefix',
            getattr(self, 'linked_field_prefix', 'id_')
        )

        return attrs

    def get_linked_fields(self):
        """
        Returns the names of fields whose values should be sent along with
        other query params during every ajax fetch.
        """
        if getattr(self, 'form', None):
            return self.form.base_fields.keys()
        return []

    def set_to_cache(self):
        """
        Add widget's attributes to Django's cache.

        Unlike Django-Select2, does not store QuerySet.
        """
        # Call `get_queryset` just to make sure widget is properly configured
        form = self.form({})
        form.is_valid()
        self.get_queryset(form)

        cache.set(self._get_cache_key(), {
            'queryset': [None, None],
            'cls': self.__class__,
            'search_fields': self.search_fields,
            'max_results': self.max_results,
            'url': self.get_url(),
            'form': self.form,
        })

    def filter_queryset(self, term, queryset=None, linked_fields=None):
        """
        Return QuerySet filtered by search_fields matching the passed term.

        Args:
        term (str): Search term.
        queryset (QuerySet): Basic QuerySet instance.
        linked_fields (dict): Map of linked keys and their values.

        Returns:
            QuerySet: Filtered QuerySet
        """
        form = self.form(linked_fields or {})
        form.is_valid()

        if queryset is None:
            queryset = self.get_queryset(form)
            if queryset is None:
                return []
        search_fields = self.get_search_fields(form)
        select = Q()
        term = term.replace('\t', ' ')
        term = term.replace('\n', ' ')
        for t in [t for t in term.split(' ') if not t == '']:
            select &= reduce(lambda x, y: x | Q(**{y: t}), search_fields,
                             Q(**{search_fields[0]: t}))
        return queryset.filter(select).distinct()

    def get_queryset(self, form):
        """
        Return QuerySet based on :attr:`.queryset` or :attr:`.model`.
        Args:
        form (Form): Form containing the linked field values.

        Returns:
            QuerySet: QuerySet of available choices.
        """
        if self.queryset is not None:
            queryset = self.queryset
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise NotImplementedError(
                '%(cls)s is missing a QuerySet. Define '
                '%(cls)s.model, %(cls)s.queryset, or override '
                '%(cls)s.get_queryset to utilize "form".' % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset

    def get_search_fields(self, form):
        """Return list of lookup names."""
        if self.search_fields:
            return self.search_fields
        raise NotImplementedError(
            '%s must implement "search_fields" or override '
            'get_search_fields().' % self.__class__.__name__
        )

    def render_options(self, *args):
        """
        Render only selected options and set QuerySet from
        :class:`ModelChoicesIterator`.
        """
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {force_text(v) for v in selected_choices}
        if not self.is_required and not self.allow_multiple_selected:
            output = ['<option></option>']
        else:
            output = ['']
        if isinstance(self.choices, ModelChoiceIterator):
            if not self.queryset:
                self.queryset = self.choices.queryset
            selected_choices = {
                c
                for c in selected_choices
                if c not in self.choices.field.empty_values
            }
            choices = {
                (obj.pk, self.label_from_instance(obj))
                for obj in self.choices.queryset.filter(
                    pk__in=selected_choices)
            }
        else:
            choices = {
                (k, v)
                for k, v in choices
                if force_text(k) in selected_choices
            }
        for option_value, option_label in choices:
            output.append(
                self.render_option(
                    selected_choices, option_value, option_label)
            )
        return '\n'.join(output)

    def label_from_instance(self, obj):
        """
        Return option label representation from instance.

        Can be overridden to change the representation of each choice.

        Example usage::

            class MyWidget(ModelSelect2Widget):
                def label_from_instance(obj):
                    return force_text(obj.title).upper()

        Args:
            obj (django.db.models.Model): Instance of Django Model.

        Returns:
            str: Option label.

        """
        return force_text(obj)


class LinkedModelSelect2Widget(
        LinkedModelSelect2Mixin, HeavySelect2Widget):
    pass


class LinkedModelSelect2MultipleWidget(
        LinkedModelSelect2Mixin, HeavySelect2MultipleWidget):
    """
    Select2 drop in model multiple select widget.

    Works just like :class:`.ModelSelect2Widget` but for multi select.
    """
    pass


class LinkedModelSelect2TagWidget(
        LinkedModelSelect2Mixin, HeavySelect2TagWidget):
    pass
