# -*- coding: UTF-8 -*-
"""
    Created by Régis Eduardo Crestani <regis.crestani@gmail.com> on 05/07/2016.
"""
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone

from . import reports, models, settings

import pygal


def charts_map(request):
    return render(request, 'django_usage/charts_map.html', context={
        'general_charts': [
            ('most-requested', 'Most requested'),
            ('most-bytes', 'Most bytes'),
            ('most-bytes-average', 'Most bytes (AVG)'),
            ('most-used-bytes', 'Most used bytes'),
            ('most-used-bytes-average', 'Most used bytes (AVG)'),
            ('most-latency', 'Most latency'),
            ('most-latency-average', 'Most latency (AVG)'),
            ('most-used-latency', 'Most used latency'),
            ('most-used-latency-average', 'Most used latency (AVG)'),
        ],
        'historical_charts': [
        ]
    })


def render_chart(data: tuple):
    chart = pygal.Bar()
    for x, y in zip(*data):
        chart.add(x, y)
    return chart.render(disable_xml_declaration=True)


def render_chart_data(request, process_data):
    try:
        count = int(request.GET['count'])
        days = int(request.GET['days'])
    except Exception:
        count = 10
        days = 30

    queryset = models.RequestRawData.objects.using(settings.DJANGO_USAGE_SETTINGS['DATABASE'])
    created_at_ref = timezone.now() - timedelta(days=days)
    return render(request, 'django_usage/chart.html', context={
        'chart_data': render_chart(process_data(queryset.filter(created_at__gte=created_at_ref), count=count))
    })


def most_requested(request):
    return render_chart_data(request, reports.most_requested)


def most_bytes(request):
    return render_chart_data(request, reports.most_bytes)


def most_bytes_average(request):
    return render_chart_data(request, reports.most_bytes_average)


def most_used_bytes(request):
    return render_chart_data(request, reports.most_used_bytes)


def most_used_bytes_average(request):
    return render_chart_data(request, reports.most_used_bytes_average)


def most_latency(request):
    return render_chart_data(request, reports.most_latency)


def most_latency_average(request):
    return render_chart_data(request, reports.most_latency_average)


def most_used_latency(request):
    return render_chart_data(request, reports.most_used_latency)


def most_used_latency_average(request):
    return render_chart_data(request, reports.most_used_latency_average)
