# -*- coding:/ utf-8 -*-
import datetime
import json
from math import floor
from random import randint
from time import mktime, time

import requests
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from yamlfield.fields import YAMLField

SOURCE_TYPES = (
    ('dummy', _('Test data')),
    ('graphite', _('Graphite')),
    ('influxdb', _('InfluxDB')),
    ('opentsdb', _('OpenTSDB')),
)

TIME_UNITS = (
    ('second', _('seconds')),
    ('minute', _('minutes')),
    ('hour', _('hours')),
    ('day', _('days')),
)

STEP_FUNS = (
    ('sum', _('sum')),
    ('avg', _('average')),
    ('min', _('minimum')),
    ('max', _('maximum')),
)


@python_2_unicode_compatible
class QuantitativeDataSource(models.Model):
    type = models.CharField(max_length=255, verbose_name=_(
        "type"), default='graphite', choices=SOURCE_TYPES)
    name = models.CharField(max_length=255, verbose_name=_("name"))
    data = YAMLField(verbose_name=_("data"), help_text=_(
        'For graphite set: host, port, ssl, user, passwd'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Quantitative data source")
        verbose_name_plural = _("Quantitative data sources")


@python_2_unicode_compatible
class QuantitativeData(models.Model):
    data_source = models.ForeignKey(
        QuantitativeDataSource, verbose_name=_('data source'))
    metrics = models.TextField(verbose_name=_("metrics"))

    def __str__(self):
        metrics = (self.metrics[:80] +
                   '..') if len(self.metrics) > 80 else self.metrics
        return "%s: %s" % (self.data_source.name, metrics)

    class Meta:
        verbose_name = _("Quantitative data")
        verbose_name_plural = _("Quantitative data")

    @cached_property
    def host(self):
        return self.get_host()

    def get_host(self):
        if self.data_source.type == 'graphite':
            if self.data_source.data.get('ssl', False):
                protocol = 'https'
            else:
                protocol = 'http'
            return '%s://%s:%s' % (protocol, self.data_source.data['host'], self.data_source.data['port'])


class TemporalDataWidget(Widget):

    data = models.ForeignKey(QuantitativeData, verbose_name=_(
        'graph'), blank=True, null=True)
    step_length = models.IntegerField(verbose_name=_('step length'), default=1)
    step_unit = models.CharField(max_length=55, verbose_name=_(
        'step unit'), choices=TIME_UNITS, default="minute")
    step_fun = models.CharField(max_length=55, verbose_name=_(
        'step function'), choices=STEP_FUNS, default="avg")
    start = models.DateTimeField(verbose_name=_(
        'start time'), blank=True, null=True)
    align_to_from = models.BooleanField(
        verbose_name=_('Align to from'), default=False)

    @cached_property
    def relative_end(self):
        if self.start:
            return str(floor(
                mktime(self.start.timetuple()) + floor(self.get_duration_delta()))).rstrip('0').rstrip('.')

    @cached_property
    def relative_start(self):
        '''returns relative start if is set'''
        if self.start:
            return str(floor(
                mktime(self.start.timetuple()) - floor(self.get_duration_delta()))).rstrip('0').rstrip('.')

        return str(floor(
            time() - self.get_duration_delta())).rstrip('0').rstrip('.')

    @cached_property
    def source(self):
        return self.data.data_source

    @cached_property
    def refresh_interval(self):
        '''returns interval in seconds'''
        return int(datetime.timedelta(**{
            self.step_unit + 's': self.step_length
        }).total_seconds())

    @cached_property
    def get_data_url(self):
        try:
            url = reverse_lazy('vislab_data')
        except:
            raise Exception('We cannot find the url for data,'
                            'have you a app mapped on some url :')
        else:
            return url

    def get_step_delta(self):
        return str(datetime.timedelta(**{
            self.step_unit + 's': self.step_length
        }).total_seconds()).rstrip('0').rstrip('.')

    def get_step_label(self):
        if self.step_unit == 'day':
            return 'd'
        if self.step_unit == 'hour':
            return 'h'
        if self.step_unit == 'minute':
            return 'm'
        if self.step_unit == 'second':
            return 's'
        return '?'

    def get_graphite_data(self, row=None, **kwargs):
        url = "%s/render" % self.data.get_host()
        data = []

        for metric in self.get_metrics(row=row):
            target = 'summarize({}, "{}s", "{}")'.format(
                metric["target"],
                self.get_step_delta(),
                self.step_fun)

            params = {
                "format": "json",
                "from": self.relative_start,
                "target": target,
            }

            if self.start:
                params['until'] = self.relative_end

            request = requests.get(url, params=params)
            json_dict = json.loads(request.text)
            values = []
            for item in json_dict[0]['datapoints'][:-1]:
                values.append({
                    'x': item[1],
                    'y': item[0],
                })
            datum = {
                'key': metric['name'],
                'values': values
            }
            data.append(datum)

        return data

    def get_update_graphite_data(self, row=None, **kwargs):
        data = self.get_graphite_data(row, **kwargs)
        for datum in data:
            datum['values'] = datum['values'][-1:]
            if 'expected_timestamp' in kwargs:
                datum['method'] = 'update'
                if kwargs['expected_timestamp'] != datum['values'][0]['x']:
                    datum['offset'] = kwargs['expected_timestamp'] - \
                        datum['values'][0]['x']
                    datum['values'][0]['x'] = kwargs['expected_timestamp']
        return data

    @cached_property
    def get_chart_params(self):
        return {
            'chartSelector': "#vis_%s" % self.fe_identifier,
            'containerSelector': "#%s" % self.fe_identifier,
            'url': str(self.get_data_url),
            'requestData': {
                'widget_id': self.fe_identifier
            },
            'updateInterval': self.refresh_interval * 1000
        }

    def get_metrics(self, row=None):
        metrics = self.data.metrics.split("\n")
        ret = []
        for metric in [metrics[int(row)]] if row is not None else metrics:
            if metric.strip('\n').strip('\r') != '':
                line = metric.strip('\n').strip('\r').split('|')
                final_line = {
                    'target': line[0],
                    'unit': line[1],
                    'name': line[2]
                }
                if len(line) > 6:
                    final_line['type'] = line[3]
                    final_line['x'] = line[4]
                    final_line['y'] = line[5]
                    final_line['scale'] = line[6]
                    if len(line) > 7:
                        final_line['horizon'] = line[7]
                ret.append(final_line)
        return ret

    def get_data(self, request, **kwargs):
        '''Returns all widget data in array or dictionary
        method must accepts ``kwargs`` where the request is
        and other kwargs which are used for advance cases
        '''
        return self.get_graph_data(**kwargs)

    def get_update_data(self, request, **kwargs):
        '''Returns part of widget data in array or dictionary
        method must accepts ``kwargs`` where the request is
        and other kwargs which are used for advance cases
        such as filtering etc.

        You can make your custom method which will be available
        for calling from fronted side and this is just an example
        how to achieve that
        '''
        if self.data is not None:
            return getattr(self,
                           'get_update_%s_data' % self.data.data_source.type,
                           self.get_graph_data)(**kwargs)

    def get_graph_data(self, **kwargs):
        '''returns data by source type
        '''
        if self.data is not None:
            return getattr(self,
                           'get_%s_data' % self.data.data_source.type
                           )(**kwargs)

    @cached_property
    def cache_data_key(self):
        '''default key for data content'''
        return 'widget.%s.data' % self.fe_identifier

    @cached_property
    def cache_keys(self):
        '''Returns all cache keys which would be
        flushed after save
        '''
        return [self.cache_key,
                self.cache_data_key + '.get_data',
                self.cache_data_key + '.get_update_data']

    class Meta:
        abstract = True


class TimeSeriesWidget(TemporalDataWidget):
    """
    Time-series widget mixin.
    """
    duration_length = models.IntegerField(
        verbose_name=_('duration length'), default=2)
    duration_unit = models.CharField(max_length=55, verbose_name=_(
        'duration unit'), choices=TIME_UNITS, default="hour")
    low_horizon = models.IntegerField(
        verbose_name=_('low horizon'), blank=True, null=True)
    high_horizon = models.IntegerField(
        verbose_name=_('high horizon'), blank=True, null=True)

    def get_value_format(self):

        if self.high_horizon:
            if self.high_horizon > 100:
                value_format = "s"
            if self.high_horizon > 10:
                value_format = ".1r"
            if self.high_horizon > 1:
                value_format = ".2r"
            else:
                value_format = ".3r"
        else:
            value_format = ""

        return value_format

    def get_time_format(self):

        duration = self.get_duration_delta()
        year = datetime.timedelta(days=365).total_seconds()
        month = datetime.timedelta(days=30).total_seconds()
        day = datetime.timedelta(days=1).total_seconds()
        minute = datetime.timedelta(minutes=1).total_seconds()

        if duration > year:
            time_format = "%b %y"
        elif duration > month:
            time_format = "%e %b"
        elif duration > day * 5:
            time_format = "%e %b"
        elif duration > minute * 30:
            time_format = "%H:%M"
        else:
            time_format = "%H:%M:%S"

        return time_format

    @cached_property
    def get_chart_params(self):

        super_data = super(TimeSeriesWidget, self).get_chart_params
        data = {
            'timeFormat': self.get_time_format(),
            'valueFormat': self.get_value_format(),
            'sendTimestamps': True
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    def get_duration_delta(self):
        return datetime.timedelta(**{
            self.duration_unit + 's': self.duration_length
        }).total_seconds()

    def get_step_count(self):
        return int(self.get_duration_delta() / int(self.get_step_delta()))

    def get_dummy_data(self, **kwargs):
        return [{
                'key': 'dummy',
                'values': [{'x': time(), 'y': randint(0, 100)}
                           for i in range(0, self.get_step_count())]
                }]

    def get_update_dummy_data(self, **kwargs):
        return [{
                'key': 'dummy',
                'values': [{'x': time(), 'y': randint(0, 100)}]
                }]

    class Meta:
        abstract = True


class NumericWidget(TemporalDataWidget):
    """
    NumericValue widget mixin.
    """
#    low_horizon = models.IntegerField(
#        verbose_name=_('low horizon'), blank=True, null=True)
#    high_horizon = models.IntegerField(
#        verbose_name=_('high horizon'), blank=True, null=True)

    @cached_property
    def relative_start(self):
        '''returns relative start if is set'''
        if self.start:
            return str(floor(
                mktime(self.start.timetuple()) - float(self.get_step_delta()))).rstrip('0').rstrip('.')

        return str(floor(
            time() - float(self.get_step_delta()))).rstrip('0').rstrip('.')

    @cached_property
    def relative_end(self):
        if self.start:
            return str(floor(
                mktime(self.start.timetuple()) + float(self.get_step_delta()))).rstrip('0').rstrip('.')

    def get_dummy_data(self, **kwargs):
        return [{'value': randint(0, 100)}]

    def get_graphite_data(self, row=None, **kwargs):
        url = "%s/render" % self.data.get_host()

        data = []

        for metric in self.get_metrics(row=row):
            target = 'summarize({}, "{}s", "{}")'.format(
                metric["target"],
                self.get_step_delta(), self.step_fun)

            params = {
                "format": "json",
                "from": self.relative_start,
                "target": target,
            }
            if self.start:
                params['until'] = self.relative_end

            request = requests.get(url, params=params)
            json_dict = json.loads(request.text)
            item_dict = {}
            for i, item in enumerate(json_dict):
                json_not_none = [x for x in item[
                    'datapoints'] if None not in x]
                if len(json_not_none) == 0:
                    # I expect this to be caused by very short step, try with longer step
                    # TODO: actually get the step and set second try step
                    # larger
                    if not item_dict and not self.start:
                        start = str(floor(
                            time() - datetime.timedelta(minutes=5).total_seconds())).rstrip('0').rstrip('.')
                        params['from'] = start
                        wide_request = requests.get(url, params=params)
                        values_dict = json.loads(wide_request.text)
                        item_dict = values_dict
                    not_none = [x for x in item_dict[i]
                                ['datapoints'] if None not in x]
                    value = 0
                    if len(not_none) > 0:
                        value = not_none[-1][0]
                    data.append({
                        'label': metric['name'],
                        'value': value
                    })
                else:
                    try:
                        data.append({
                            'value': reduce(
                                lambda x, y: x[0] + y[0],
                                json_not_none)[0] / len(json_not_none),
                            'label': metric['name']
                        })
                    except:
                        try:
                            data.append({
                                'value': reduce(
                                    lambda x, y: x[0] + y[0],
                                    json_not_none) / len(json_not_none),
                                'label': metric['name']
                            })
                        except:
                            data.append({
                                'value': reduce(
                                    lambda x, y: x + y,
                                    [x[0] for x in json_not_none]) / len(json_not_none),
                                'label': metric['name']
                            })
        return data

    def get_update_graphite_data(self, row=None, **kwargs):
        return self.get_graphite_data(row, **kwargs)

    def get_dummy_data(self, **kwargs):
        data = []
        for metric in self.get_metrics():
            data.append({
                'label': metric['name'],
                'value': randint(0, 200)
            })
        return data

    def get_update_dummy_data(self, **kwargs):
        data = []
        for metric in self.get_metrics():
            data.append({
                'label': metric['name'],
                'value': randint(0, 200)
            })
        return data

    class Meta:
        abstract = True

#    tabs = {
#        'Format': {
#            'name': _('Format'),
#            'fields': ('duration_length', 'duration_unit',
#                       'low_horizon', 'high_horizon')
#        },
#        'Data': {
#            'name': _('Data'),
#            'fields': ('step_length', 'step_length',
#                       'step_unit', 'step_fun',
#                       'start', 'align_to_from')
#        }
#    }
