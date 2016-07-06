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
            ('most-requested-with-status', 'Most requested (With status)'),
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
            ('requests-by-date', 'Requests count by date'),
            ('used-bytes-average-by-date', 'Bytes by date (AVG)'),
            ('used-bytes-avg-min-max-by-date', 'Bytes by date (AVG|MIN|MAX)'),
            ('used-latency-average-by-date', 'Latency by date (AVG)'),
            ('used-latency-avg-min-max-by-date', 'Latency by date (AVG|MIN|MAX)'),
        ]
    })


def render_chart(data):
    chart = pygal.Bar()
    for x, y in zip(*data):
        chart.add(x, y)
    return chart.render(disable_xml_declaration=True)


def render_historical_chart(data):
    chart = pygal.StackedLine(fill=True)
    chart.x_labels = data['X-LABELS']
    del data['X-LABELS']
    for name, entry_data in data.items():
        chart.add(name, entry_data[reports.Y_POS])
    return chart.render(disable_xml_declaration=True)


def render_chart_data(request, process_data, process_render_chart=render_chart):
    try:
        count = int(request.GET['count'])
    except Exception:  # case user inputs an invalid int
        count = 10
    try:
        offset = int(request.GET['offset'])
    except Exception:  # case user inputs an invalid int
        offset = 0
    try:
        days = int(request.GET['days'])
    except Exception:  # case user inputs an invalid int
        days = 30

    queryset = models.RequestRawData.objects.using(settings.DJANGO_USAGE_SETTINGS['DATABASE'])
    created_at_ref = timezone.now() - timedelta(days=days)
    return render(request, 'django_usage/chart.html', context={
        'chart_data': process_render_chart(process_data(queryset.filter(created_at__gte=created_at_ref),
                                                        count=count,
                                                        offset=offset))
    })


def most_requested(request):
    return render_chart_data(request, reports.most_requested)


def most_requested_with_status(request):
    def _render_chart(data):
        chart = pygal.Bar()
        chart.x_labels = data['total'][reports.X_POS]
        statuses = list(data.keys())
        statuses.sort()
        for status in statuses:
            chart.add(status, data[status][reports.Y_POS])
        return chart.render(disable_xml_declaration=True)

    return render_chart_data(request, reports.most_requested_with_status, process_render_chart=_render_chart)


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


def requests_by_date(request):
    return render_chart_data(request, reports.requests_by_date, process_render_chart=render_historical_chart)


def used_bytes_average_by_date(request):
    return render_chart_data(request, reports.used_bytes_average_by_date, process_render_chart=render_historical_chart)


def used_latency_average_by_date(request):
    return render_chart_data(request, reports.used_latency_average_by_date,
                             process_render_chart=render_historical_chart)


def used_bytes_avg_min_max_by_date(request):
    return render_chart_data(request, reports.used_bytes_avg_min_max_by_date,
                             process_render_chart=render_historical_chart)


def used_latency_avg_min_max_by_date(request):
    return render_chart_data(request, reports.used_latency_avg_min_max_by_date,
                             process_render_chart=render_historical_chart)
