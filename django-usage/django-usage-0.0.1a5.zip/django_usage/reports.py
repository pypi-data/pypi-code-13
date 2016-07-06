# -*- coding: UTF-8 -*-
"""
    Created by Régis Eduardo Crestani <regis.crestani@gmail.com> on 21/06/2016.
"""
from copy import copy

from django.db.models import Count, Sum, Avg, ExpressionWrapper, FloatField, Max, Min
from django.utils import dateparse
from datetime import timedelta

X_POS = 0
Y_POS = 1


def __build_entry_name__(entry: dict) -> str:
    return '{method}: {name}'.format(**entry)


def __build_xy__(queryset):
    x = []
    y = []
    for entry in queryset:
        x.append(__build_entry_name__(entry))
        y.append(entry['amount'])
    return x, y


def __build_historical_xy__(queryset):
    x = []
    y = []
    date_ref = None
    for entry in queryset:
        moment = dateparse.parse_date(entry['moment'])
        if date_ref is None:
            date_ref = moment
        else:
            date_ref += timedelta(days=1)
        while moment > date_ref:
            x.append(date_ref.strftime('%Y-%m-%d'))
            y.append(0)
            date_ref += timedelta(days=1)
        x.append(entry['moment'])
        y.append(entry['amount'])
    return x, y


def most_requested(queryset, count=10, offset=0) -> tuple:
    queryset = queryset.values('name', 'method').annotate(amount=Count('id')).order_by('-amount')
    return __build_xy__(queryset[offset:offset + count])


def most_requested_with_status(queryset, count=10, offset=0) -> dict:
    total = most_requested(queryset, count=count)
    total_x = total[X_POS]
    cleaned_y = [0 for _ in range(len(total[X_POS]))]
    report = {'total': total}
    for status in queryset.values_list('status', flat=True).distinct():
        report[str(status)] = (total_x, copy(cleaned_y))
    queryset = queryset.values('name', 'method', 'status').annotate(amount=Count('id')).order_by('-amount')
    for entry in queryset[offset:offset + count]:
        name = __build_entry_name__(entry)
        entry_report = report[str(entry['status'])]
        x = entry_report[X_POS]
        y = entry_report[Y_POS]

        try:
            y[x.index(name)] = entry['amount']
        except ValueError:
            pass

    return report


def most_bytes(queryset, count=10, offset=0) -> tuple:
    q_set = queryset.values('name', 'method').annotate(amount=Sum('size')).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_bytes_average(queryset, count=10, offset=0) -> tuple:
    q_set = queryset.values('name', 'method').annotate(amount=Avg('size')).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_used_bytes(queryset, count=10, offset=0) -> tuple:
    expression = ExpressionWrapper(Sum('size') * Count('id'), output_field=FloatField())
    q_set = queryset.values('name', 'method').annotate(amount=expression).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_used_bytes_average(queryset, count=10, offset=0) -> tuple:
    expression = ExpressionWrapper(Avg('size') * Count('id'), output_field=FloatField())
    q_set = queryset.values('name', 'method').annotate(amount=expression).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_latency(queryset, count=10, offset=0) -> tuple:
    q_set = queryset.values('name', 'method').annotate(amount=Sum('latency')).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_latency_average(queryset, count=10, offset=0) -> tuple:
    q_set = queryset.values('name', 'method').annotate(amount=Avg('latency')).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_used_latency(queryset, count=10, offset=0) -> tuple:
    expression = ExpressionWrapper(Sum('latency') * Count('id'), output_field=FloatField())
    q_set = queryset.values('name', 'method').annotate(amount=expression).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def most_used_latency_average(queryset, count=10, offset=0) -> tuple:
    expression = ExpressionWrapper(Avg('latency') * Count('id'), output_field=FloatField())
    q_set = queryset.values('name', 'method').annotate(amount=expression).order_by('-amount')[offset:offset + count]
    return __build_xy__(q_set)


def requests_by_date(queryset, count=30, offset=0) -> dict:
    q_set = queryset.extra(select={'moment': 'date(created_at)'}).values('moment').annotate(amount=Count('id'))
    data = {'Count': __build_historical_xy__(q_set.order_by('-moment')[offset:offset + count].reverse())}
    data['X-LABELS'] = data['Count'][X_POS]
    return data


def used_bytes_average_by_date(queryset, count=30, offset=0) -> dict:
    _select = {'moment': 'date(created_at)'}
    avg_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Avg('size'))
    data = {
        'Average': __build_historical_xy__(avg_queryset.order_by('-moment')[offset:offset + count].reverse())
    }
    data['X-LABELS'] = data['Average'][X_POS]
    return data


def used_latency_average_by_date(queryset, count=30, offset=0) -> dict:
    _select = {'moment': 'date(created_at)'}
    avg_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Avg('latency'))
    data = {
        'Average': __build_historical_xy__(avg_queryset.order_by('-moment')[offset:offset + count].reverse())
    }
    data['X-LABELS'] = data['Average'][X_POS]
    return data


def used_bytes_avg_min_max_by_date(queryset, count=30, offset=0) -> dict:
    _select = {'moment': 'date(created_at)'}
    avg_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Avg('size'))
    max_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Max('size'))
    min_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Min('size'))
    data = {
        'Average': __build_historical_xy__(avg_queryset.order_by('-moment')[offset:offset + count].reverse()),
        'Max': __build_historical_xy__(max_queryset.order_by('-moment')[offset:offset + count].reverse()),
        'Min': __build_historical_xy__(min_queryset.order_by('-moment')[offset:offset + count].reverse())
    }
    data['X-LABELS'] = data['Average'][X_POS]
    return data


def used_latency_avg_min_max_by_date(queryset, count=30, offset=0) -> dict:
    _select = {'moment': 'date(created_at)'}
    avg_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Avg('latency'))
    max_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Max('latency'))
    min_queryset = queryset.extra(select=_select).values('moment').annotate(amount=Min('latency'))
    data = {
        'Average': __build_historical_xy__(avg_queryset.order_by('-moment')[offset:offset + count].reverse()),
        'Max': __build_historical_xy__(max_queryset.order_by('-moment')[offset:offset + count].reverse()),
        'Min': __build_historical_xy__(min_queryset.order_by('-moment')[offset:offset + count].reverse())
    }
    data['X-LABELS'] = data['Average'][X_POS]
    return data
