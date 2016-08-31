"""
Google Analytics abstraction & convenience methods.

This abstraction enables reuse of valuable analytics components, e.g. segments,
from the Google Analytics V4 API, and provides consistency and clarity in p
reparing API extracts from Google Analytics, where Google's specification of
the V4 report request model is quite nuanced.


Useful classes:
    - ReportBatch({string viewId, the Analytics "view" (or profile)})
    - ReportRequestModel

The ReportBatch coordinates dispatch of multiple ReportRequestModels to Google
Analytics' reporting service.  Each Batch can have up to 5 simultaneous report
requests. A ReportBatch automatically starts with one report request.


The current report request of a given batch can be accessed as:

    batch = ReportBatch("{view-id}")
    report = batch.cursor  # current report

New report requests can be added:

    report = batch.next_report()

ReportBatch provides the following methods:
- add_date_range (required 1, allowed 2)
- add_segment
- add_cohort
- build_segment
- build_simple_segment
- build_sequence_segment
- build_segment_filter_group
- build_segement_sequence_step
- build_segment_filter_dimension_clause
- build_segment_filter_metric_clause
- build_cohort

ReportRequestModel provides the following methods:
- include_empty_rows
- hide_total_summary
- hide_value_ranges
- add_dimension
- add_metric
- add_pivot
- add_dimension_filters
- add_metric_filters
- build_dimension_filter
- build_metric_filter
- build_pivot_clause
- build_dimension_clause
- build_metric_clause
- order_by
- set_page_size
- set_filter


Sensible use of Google Analytics API is beyond the scope of this document.
An example (from our test kit) provides some clarity on the use of these
various functionality:

    batch = ReportBatch("abc123")   # the (viewId == abc123) for test.
    report = batch.cursor

    batch.add_date_range('2016-01-01', '2016-01-28')
    batch.add_date_range('2016-02-01', '2016-02-28')

    report.add_dimension("ga:city")
    report.add_dimension("ga:landingPage")
    report.add_metric("ga:timeOnSite")

    report.add_metric_filters([
        report.build_metric_filter("ga:timeOnSite", "60",
                                   operator='GREATER_THAN')
    ])

    report.add_dimension_filters([
        report.build_dimension_filter("ga:landingPage", '^/blog/')
    ])

    report.add_pivot(report.build_pivot_clause(
        [report.build_metric_clause("ga:pageviews")],
        [report.build_dimension_clause("ga:page")],
        dim_filters=[report.build_dimension_filter("ga:page", '^/blog/')]
    ))

    batch.fetch()   # dispatch the query to Google



See also:
https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#metrictype
https://developers.google.com/resources/api-libraries/documentation/analyticsreporting/v4/python/latest/
https://developers.google.com/analytics/devguides/reporting/core/v4/basics#response_body
https://developers.google.com/analytics/devguides/reporting/
https://developers.google.com/analytics/devguides/config/mgmt/v3/
https://developers.google.com/resources/api-libraries/documentation/analytics/v3/python/latest/index.html
https://developers.google.com/resources/api-libraries/documentation/analyticsreporting/v4/python/latest/index.html
"""

from webapp2 import cached_property

from . import googleapi
from .util import dict_resolve, odict

# import uuid
import re
import copy
import logging

from datetime import timedelta


def mute_logger(name):
    _logger = logging.getLogger(name)
    _logger.addHandler(logging.NullHandler())
    _logger.setLevel(logging.CRITICAL)


mute_logger('oauth2client.client')
mute_logger('googleapiclient.discovery')


class GoogleAnalyticsReportingService(googleapi.ServiceBase):
    """An abstraction of the Google Analytics Reporting API version 4."""

    # TODO: enable overriding quotaUser query parameter.
    # https://developers.google.com/analytics/devguides/reporting/core/v4/parameters

    API_SCOPE = [
        'https://www.googleapis.com/auth/analytics.readonly',
        'https://www.googleapis.com/auth/analytics.edit',
        'https://www.googleapis.com/auth/analytics'
    ]

    @cached_property
    def api_v4(self):
        """The version 4 API; provides advanced reporting capabilities only."""
        url = 'https://analyticsreporting.googleapis.com/$discovery/rest'
        return self.discover('analyticsreporting', 'v4',
                             discoveryServiceUrl=url)

    @cached_property
    def api_v3(self):
        """
        The version 3 API; provides management metadata and basic reporting.

        This module relies on the V3 API primarily for management information,
        interrogating the list of accounts, properties, and profiles.
        """
        return self.discover('analytics', 'v3')

    @property
    def accounts(self):
        query = self.api_v3.management().accounts().list
        result = self.execute(query)
        for record in result.get('items', []):
            yield record.get('id'), record.get('name'), record

    def list_properties(self, account_id):
        query = self.api_v3.management().webproperties().list
        result = self.execute(query, accountId=account_id)
        for record in result.get('items', []):
            yield record.get('id'), \
                record.get('internalWebPropertyId'), \
                record.get('name'), \
                record

    def find_internal_property_id(self, account_id, web_property_id):
        for _id, _id_int, name, record in self.list_properties(account_id):
            if (_id == web_property_id):
                return _id_int

    def list_profiles(self, account_id, property_id):
        # NOTE: the GA jargon equates "views" with "profiles" (historically)
        query = self.api_v3.management().profiles().list
        result = self.execute(query,
                              accountId=account_id,
                              webPropertyId=property_id)
        for record in result.get('items', []):
            yield record.get('id'), \
                record.get('name'), \
                record

    @property
    def profiles(self):  # noqa
        """
        Generate a series of object groups representing all available data
        sources (sets of [account->property->profile]).

        This list could get quite large. Some high-volume consultants observe
        multiple hundreds of accounts; each account can have up to 50
        properties, and each property can have up to 50 views/profiles.
        Altogether this might approximate (1000*50*50), though it will be rare.
        """
        for account_id, account_name, account in self.accounts:
            webproperties = self.list_properties(account_id)
            for prop_alias, prop_id, prop_name, prop in webproperties:
                profiles = self.list_profiles(account_id, prop_alias)
                for prof_id, prof_name, prof in profiles:
                    yield odict(
                        ident=(account_id, prop_id, prof_id),
                        account=account,
                        webproperty=prop,
                        profile=prof,
                        account_name=account_name,
                        webproperty_name=prop_name,
                        webproperty_alias=prop_alias,
                        profile_name=prof_name
                    )

RE_TIME_DURATION = re.compile('^([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})$')


def coerce_type(typename, value, name):
    assert isinstance(value, basestring), \
        ("Expected string, got %r for %r" % (type(value), name))
    if typename in ('INTEGER',):
        return int(value)
    if typename in ('FLOAT', 'CURRENCY', 'PERCENT'):
        return float(value)
    if typename in ('TIME',):
        parts = RE_TIME_DURATION.match(value)
        h, m, s = parts.group(1, 2, 3)
        return timedelta(hours=h, minutes=m, seconds=s)
    return value  # type unknown...


class ReportProxy(object):
    """Accessor to the Google Analytics report model returned by the API."""

    def __init__(self, report_base):
        self.base = report_base

    @property
    def has_pivot(self):
        return bool(len(self.pivot_headers_raw))

    @property
    def pivot_headers_raw(self):
        expr = 'columnHeader.metricHeader.pivotHeaders'
        return dict_resolve(self.base, expr, [])

    @property
    def dimension_headers(self):
        return self.base.get('columnHeader', {}).get('dimensions')  # strings

    @property
    def pivot_headers(self):
        pivots = self.pivot_headers_raw
        entries = [p.get('pivotHeaderEntries', []) for p in pivots]

        for entry_group in entries:
            for entry in entry_group:
                names = entry.get('dimensionNames', [])
                values = entry.get('dimensionValues', [])
                dim = zip(names, values)
                met = entry.get('metric', {})

                # A tuple of ({tuple<name, val>}, {string}, {string})
                yield dim, met.get('name'), met.get('type')

    @property
    def metric_headers(self):
        columns = self.base.get('columnHeader', {})
        columns_met = columns.get('metricHeader', {})
        for met in columns_met.get('metricHeaderEntries', []):
            # A tuple of ({string}, {string})
            yield met.get('name'), met.get('type')

    @property
    def data(self):
        return self.base.get('data', {})

    @staticmethod
    def bind_metrics(values, names, types):
        for i, val in enumerate(values):
            # Tuples of ({string}, {numeric|timedelta|string})
            yield (names[i], coerce_type(types[i], val, names[i]))

    @staticmethod
    def bind_pivots(pivot_values, dimensions, names, types):
        for i, val in enumerate(pivot_values):
            # Tuples of ({dict}, {string}, {numeric|timedelta|string})
            yield (dict(dimensions[i]), names[i],
                   coerce_type(types[i], val, names[i]))

    @property
    def rows(self):
        _rows = self.data.get('rows', [])
        headers_dim = list(self.dimension_headers)
        headers_met = list(self.metric_headers)
        headers_piv = list(self.pivot_headers)

        met_names, met_types = zip(*headers_met)

        if len(headers_piv):
            piv_dim, piv_names, piv_types = zip(*headers_piv)

        def bp(p):  # shorthand for binding pivots
            return self.bind_pivots(p, piv_dim, piv_names, piv_types)

        for r in _rows:
            dimensions = zip(headers_dim, r.get('dimensions', []))

            for m in r.get('metrics', []):
                plain = m.get('values', [])  # the raw sequence of metric val
                plain = self.bind_metrics(plain, met_names, met_types)

                if len(headers_piv):
                    pivot = m.get('pivotValueRegions', [])  # those for pivots
                    pivot = [p.get('values') for p in pivot]
                    pivot = [list(bp(p)) for p in pivot]

                else:
                    pivot = None

                yield dimensions, list(plain), pivot

    def __iter__(self):
        return self.rows


class ReportBatch():

    RE_DATE_FORMAT = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    def __init__(self, view_id=None):
        self.view_id = view_id
        self.reports = [ReportRequestModel()]
        self.report_index = 0
        self.cohort_group = []  # (requires dimension ga:cohort)
        self.sampling_level = 'DEFAULT'
        self.use_lifetime_value = False
        self.date_ranges = []
        self.segments = []

    def next_report(self):
        """Add a report model and iterate the cursor."""
        self.reports.append(ReportRequestModel())
        self.report_index = len(self.reports) - 1
        return self.cursor

    @classmethod
    def clone(cls, instance):
        _new = cls(instance.view_id)
        _new.reports = [r.clone(r) for r in instance.reports]
        _new.cohort_group = copy.deepcopy(instance.cohort_group)
        _new.date_ranges = copy.deepcopy(instance.date_ranges)
        _new.segments = copy.deepcopy(instance.segments)
        _new.use_lifetime_value = instance.use_lifetime_value
        _new.report_index = instance.report_index
        _new.sampling_level = instance.sampling_level
        return _new


    @property
    def cursor(self):
        """Shortcut access to the current report."""
        return self.reports[self.report_index]

    def set_sampling_level(self, level):
        assert (level in ('DEFAULT', 'SMALL', 'LARGE'))
        self.sampling_level = level

    err_wrong_date = 'Dates must be strings formated YYYY-MM-DD.'

    def add_segment(self, *segments):
        for s in segments:
            assert isinstance(s, (basestring, dict))
            if isinstance(s, basestring):
                self.segments.append(dict(segmentId=s))
            elif isinstance(s, dict):
                self.segments.append(dict(dynamicSegment=s))

    @classmethod
    def build_segment(cls, name, sessions=None, users=None):
        """
        Combine segment components.

        The segment definition permits _both_ user and session filter
        declaration in a single segment.
        """
        base = dict(name=name)
        if isinstance(sessions, dict):
            sessions = [sessions]
        if isinstance(users, dict):
            users = [users]
        if isinstance(sessions, list):
            base['sessionSegment'] = dict(segmentFilters=sessions)
        if isinstance(users, list):
            base['userSegment'] = dict(segmentFilters=users)

        assert ('userSegment' in base) or ('sessionSegment' in base)
        return base

    @classmethod
    def build_simple_segment(cls, *and_groups, **kwargs):
        """
        Assemble a simple segment.

        Each argument should be a list of segment filter clauses, as defined by
        either:
            - build_segment_filter_dimension_clause
            - build_segment_filter_metric_clause

        Each list argument's filters will be OR'ed together, and the group of
        all lists will be AND'ed together.

        Example:
            build_simple_segment([A, B], [C, D])
            >> will produce a segment of all (Sessions or Users) which are:
                - (A or B) and (C or D)
        """
        base = dict(simpleSegment=cls.build_segment_filter_group(and_groups))
        base['not'] = bool(kwargs.pop('invert', False))
        return base

    @classmethod
    def build_segment_filter_group(cls, and_groups):
        or_filters = [dict(segmentFilterClauses=a) for a in and_groups]
        return dict(orFiltersForSegment=or_filters)

    @classmethod
    def build_sequence_segment(cls, *steps, **kwargs):
        match_first = bool(kwargs.pop('match_first', False))
        base = dict(sequenceSegment=dict(
            firstStepShouldMatchFirstHit=match_first,
            segmentSequenceSteps=steps
        ))
        base['not'] = bool(kwargs.pop('invert', False))
        return base

    @classmethod
    def build_segment_sequence_step(cls, match_type, *and_groups):
        """Construct the segment step with a series of constraints.

        The match_type is specified in relation to any following step.
        The and_groups list
        """
        assert (match_type in ('PRECEDES', 'IMMEDIATELY_PRECEDES'))
        base = cls.build_segment_filter_group(and_groups)
        base['matchType'] = match_type
        return base

    @classmethod
    def build_segment_filter_dimension_clause(cls, dimension, operator, value,
                                              invert=False,
                                              case_sensitive=False):
        """
        Construct a dimension filter for a segment.

        Operators:
        https://developers.google.com/analytics/devguides/reporting/core/v3/segments#operators
        """
        assert (operator in (
            'EXACT', 'REGEXP', 'BEGINS_WITH', 'ENDS_WITH', 'PARTIAL',
            'NUMERIC_BETWEEN', 'NUMERIC_GREATER_THAN', 'NUMERIC_LESS_THAN',
            'IN_LIST'
        ))

        expr = ([value] if isinstance(value, basestring) else value)

        filter_def = dict(
            dimensionName=dimension,
            operator=operator,
            caseSensitive=bool(case_sensitive),
            expressions=expr
        )

        if operator in ('NUMERIC_BETWEEN'):
            _min, _max = value
            filter_def['minComparisonValue'] = _min
            filter_def['maxComparisonValue'] = _max

        base = dict(dimensionFilter=filter_def)
        base['not'] = bool(invert)
        return base

    @classmethod
    def build_segment_filter_metric_clause(cls, metric, scope, operator, value,
                                           invert=False):

        assert (operator in ('EQUAL', 'LESS_THAN', 'GREATER_THAN', 'BETWEEN'
                             'IS_MISSING'))

        assert (scope in ('USER', 'SESSION', 'HIT', 'PRODUCT'))

        if operator == 'BETWEEN':
            _min, _max = value
        else:
            _min, _max = value, None

        filter_def = dict(
            metricName=metric,
            operator=operator,
            scope=scope,
            comparisonValue=str(_min),
            maxComparisonValue=str(_max or 0)
        )

        base = dict(metricFilter=filter_def)
        base['not'] = bool(invert)
        return base

    @classmethod
    def build_cohort(cls, name, date_start, date_end,
                     cohort_type='FIRST_VISIT_DATE'):

        # NOTE only FIRST_VISIT_DATE is supported for cohort type a this time.
        # Eventually other cohort models may be supported.
        assert (cohort_type in ('FIRST_VISIT_DATE',))

        return dict(
            name=name,
            dateRange=cls.build_date_range(date_start, date_end),
            type=cohort_type
        )

    def add_cohort(self, *cohorts):
        # NOTE: using cohorts restricts the available dimensions and metrics.
        # https://developers.google.com/analytics/devguides/reporting/core/v4/advanced#dimensions
        for c in cohorts:
            assert isinstance(c, dict)
            self.cohort_group.append(c)

    @classmethod
    def build_date_range(cls, _begin, _end):
        assert cls.RE_DATE_FORMAT.match(_begin), cls.err_wrong_date
        assert cls.RE_DATE_FORMAT.match(_end), cls.err_wrong_date
        return dict(startDate=_begin, endDate=_end)

    def add_date_range(self, _begin, _end):
        self.date_ranges.append(self.build_date_range(_begin, _end))

    def to_dict(self, view_id):
        """Construct the query body for a batch and assimilate reports."""
        assert isinstance(view_id, basestring)
        assert (0 < len(self.reports) < 6), \
            "A report batch allows 1 to 5 reports simultaneous."
        assert (len(self.cohort_group)) or (0 < len(self.date_ranges) < 3), \
            "A report batch requires one or two (maximum) date ranges."
        assert (0 <= len(self.segments) < 5), \
            "A report batch allows a maximum of 4 segments."

        if len(self.cohort_group):  # Construct cohort configuration.
            cohort_config = dict(
                cohorts=self.cohort_group,
                lifetimeValue=bool(self.use_lifetime_value)
            )
            # activate dimension "ga:cohort" when cohorts in play.
            for r in self.reports:
                r.add_dimension("ga:cohort")
        else:
            cohort_config = None

        if len(self.segments):
            # activate dimension "ga:segment" when segments in play.
            for r in self.reports:
                r.add_dimension("ga:segment")

        # Collect all the subordinate report component.s
        reports = [r.to_dict(view_id) for r in self.reports]

        # Apply the batch-level properties that must be consistent.
        for r in reports:
            r['cohortGroup'] = cohort_config
            r['dateRanges'] = self.date_ranges
            r['samplingLevel'] = self.sampling_level
            r['segments'] = self.segments

        return dict(reportRequests=reports)

    def fetch(self, analytics_service, *view_ids):
        """
        Issue the batch requests and generate report results.

        This method permits multiple view IDs to be provided (as a sequence of
        arguments), to run the same batch of requests against multiple data
        sets [i.e. views/profiles] within Google Analytics.

        When no view ID is provided, it will attempt to use the "default" view
        ID provided in the constructor.

        """
        assert isinstance(analytics_service, GoogleAnalyticsReportingService)
        service = analytics_service.api_v4

        if not len(view_ids):
            view_ids = [self.view_ids]
        for v in view_ids:
            if isinstance(v, basestring):
                request = service.reports().batchGet(body=self.to_dict(v))
                result = request.execute(http=analytics_service.http)
                for report in result.get('reports', []):
                    yield ReportProxy(report)


class ReportRequestModel(object):
    """
    Prepare a report model to request (as part of a batch).

    Many parameters require knowledge of the Google Analytics data model.
    Dimensions and Metrics both have "scope", and some cannot be combined due
    to scope incompatibility.

    See also:
    https://developers.google.com/analytics/devguides/reporting/core/dimsmets
    """

    def __init__(self):
        self.dimensions = []
        self.metrics = []
        self.order_by = []
        self.options = dict(   # more properties to inject...
            pageSize=10000,
            includeEmptyRows=False,
            hideTotals=False,
            hideValueRanges=False,
            dimensionFilterClauses=[],
            metricFilterClauses=[],
            pivots=[],
            orderBys=[]
        )

    @classmethod
    def clone(cls, instance):
        _new = cls()
        _new.dimensions = copy.deepcopy(instance.dimensions)
        _new.metrics = copy.deepcopy(instance.metrics)
        _new.order_by = copy.deepcopy(instance.order_by)
        _new.options = copy.deepcopy(instance.options)
        return _new

    def include_empty_rows(self):
        self.options['includeEmptyRows'] = True

    def hide_total_summary(self):
        self.options['hideTotals'] = True

    def hide_value_ranges(self):
        self.options['hideValueRanges'] = True

    @classmethod
    def build_dimension_filter(cls, dimension, *expressions, **kwargs):
        """
        Construct a component filter (dictionary) for dimensionFilterClauses.

        In many cases multiple such filters will be combined.
        """
        operator = kwargs.pop('operator', 'REGEXP')

        # NOTE this one doesn't support NUMERIC_BETWEEN
        assert (operator in (
                'REGEXP', 'IN_LIST', 'EXACT', 'PARTIAL',
                'BEGINS_WITH', 'ENDS_WITH', 'NUMERIC_EQUAL',
                'NUMERIC_GREATER_THAN', 'NUMERIC_LESS_THAN'
                ))

        base = dict(
            dimensionName=dimension,
            operator=operator,
            expressions=list(expressions),
            caseSensitive=bool(kwargs.pop('case_sensitive', False))
        )
        base['not'] = bool(kwargs.pop('invert', False))
        return base

    @classmethod
    def build_metric_filter(cls, metric, compare_value, operator='EQUAL',
                            invert=False):
        assert (operator in ('EQUAL', 'LESS_THAN', 'GREATER_THAN',
                             'IS_MISSING'))

        if operator == 'IS_MISSING':
            compare_value = None
        else:
            compare_value = str(compare_value)

        base = dict(
            metricName=metric,
            operator=operator,
            comparisonValue=compare_value
        )
        base['not'] = bool(invert)
        return base

    @classmethod
    def build_pivot_clause(cls, metrics, dimensions, dim_filters=None,
                           start=1, max_groups=10):
        assert isinstance(metrics, list)
        assert isinstance(dimensions, list)
        assert (dim_filters is None) or isinstance(dim_filters, list)
        assert (0 < max_groups <= 1000)
        return dict(
            metrics=metrics,
            dimensions=dimensions,
            startGroup=int(start),
            maxGroupCount=int(max_groups),
            dimensionFilterClauses=(dim_filters or [])
        )

    def add_pivot(self, *pivots):
        for p in pivots:
            assert isinstance(p, dict)
            self.options['pivots'].append(p)

    @classmethod
    def build_dimension_filter_clause(cls, *filters, **kwargs):
        """These filters will be logically AND-ed together."""
        operator = kwargs.pop('operator', 'OR')
        assert (operator in ('OR', 'AND', None))
        return dict(
            filters=[f for f in filters if isinstance(f, dict)],
            operator=(operator or 'OR')
        )

    def add_dimension_filters(self, *filter_group):
        for f in filter_group:
            if isinstance(f, dict):
                self.options['dimensionFilterClauses'].append(f)

    @classmethod
    def build_dimension_clause(cls, dimension_name, histogram=None):
        # https://developers.google.com/analytics/devguides/reporting/core/dimsmets
        return dict(
            name=dimension_name,
            histogramBuckets=histogram
        )

    def has_dimension(self, dimension_name):
        for d in self.dimensions:
            if d.get('name') == dimension_name:
                return True
        return False

    def add_dimension(self, *args, **kwargs):
        for a in args:
            if self.has_dimension(a):
                continue
            dim = self.build_dimension_clause(a, **kwargs)
            self.dimensions.append(dim)
            if dim.get('histogramBuckets', None):
                self.apply_order(dim.get('name'),
                                 order_type='HISTOGRAM_BUCKET')

    def add_metric_filters(self, filter_group, operator='OR'):
        assert (operator in ('OR', 'AND'))
        assert isinstance(filter_group, list)
        self.options['metricFilterClauses'].append(dict(
            filters=filter_group,
            operator=operator
        ))

    @classmethod
    def build_metric_clause(cls, expression, alias=None, format='INTEGER'):
        # https://developers.google.com/analytics/devguides/reporting/core/dimsmets
        # TODO: some reasonably intelligent auto-generate the alias
        assert (format in ('INTEGER', 'FLOAT', 'CURRENCY', 'PERCENT', 'TIME'))
        return dict(
            # can be "ga:users" or basic math like "ga:pageviews/ga:users"
            expression=expression,
            alias=alias,
            formattingType=format  # usually something like "INTEGER"
        )

    def add_metric(self, *args, **kwargs):
        self.metrics.append(self.build_metric_clause(*args, **kwargs))

    def apply_order(self, name, order_type=None, sort_order=None):
        assert (order_type in (None, 'VALUE', 'DELTA', 'SMART',
                               'HISTOGRAM_BUCKET',
                               'DIMENSION_AS_INTEGER'))
        assert (sort_order in (None, 'ASCENDING', 'DESCENDING'))
        self.options['orderBys'].append(dict(
            fieldName=name,
            orderType=(order_type or 'VALUE'),
            sortOrder=(sort_order or 'ASCENDING')
        ))

    def set_page_size(self, num_records):
        self.options['pageSize'] = int(num_records)

    def set_filter(self, *expressions):
        """
        Provide a filter expression for this report.

        Multiple (string) arguments will be treated as OR-ed filter statements.
        Individual statements can express AND using the ";" concatenator.

        Examples:
        - ga:browser=~Internet%20Explorer;ga:browserVersion==8.0  # only IE8.0
        - ga:browser=~Chrome,ga:browser=~Safari  # Chrome or Safari

        See also:
        https://developers.google.com/analytics/devguides/reporting/core/dimsmets
        https://developers.google.com/analytics/devguides/reporting/core/v3/reference#filters
        """
        # TODO validate expression? ("ga:<dim_or_prop><operator><value>")
        self.properties['filtersExpression'] = ','.join(expressions)  # OR

    def to_dict(self, view_id):
        """Prepare the report request data structure for batch transit."""
        for i, d in enumerate(self.dimensions):
            # NOTE: histogram support requires the add_dimension() method
            if isinstance(d, basestring):
                self.dimensions[i] = dict(name=d)

        for i, m in enumerate(self.metrics):
            if isinstance(m, basestring):
                self.metrics[i] = dict(expressions=m, alias=m,
                                       formattingType="FLOAT")

        assert (0 < self.options['pageSize'] < 10001)

        return dict(
            # configure-able per report request in batch
            viewId=view_id,
            metrics=self.metrics,
            dimensions=self.dimensions,
            pageToken=None,  # TODO: consider pagination.

            # inherit the object's options dictionary (for simple properties).
            **self.options

            # NB: the following must be consistent across batch!!!
            # These are now enforced by the Batch handler..
            # samplingLevel="DEFAULT",
            # dateRanges=self.date_ranges,
            # cohortGroups=[],
            # viewId=self.view_id
        )
