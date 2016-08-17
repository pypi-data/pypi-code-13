# -*- coding: utf-8 -*-
from django import forms

import django_filters
from django_filters.widgets import RangeWidget


class DateTimeRangeField(forms.MultiValueField):
    widget = RangeWidget(attrs={'class': 'datetime'})

    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateTimeField(),
            forms.DateTimeField(),
        )
        super(DateTimeRangeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


class DateTimeRangeFilter(django_filters.Filter):

    field_class = DateTimeRangeField

    def filter(self, qs, value):
        if value:
            filter_by = dict()
            if value.start:
                filter_by.update({'%s__gte' % self.name: value.start})
            if value.stop:
                filter_by.update({'%s__lte' % self.name: value.stop})
            return qs.filter(**filter_by)
        return qs
