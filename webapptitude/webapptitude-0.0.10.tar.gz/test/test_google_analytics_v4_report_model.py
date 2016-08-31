
from webapptitude.googleanalytics import (  # noqa
    ReportBatch, ReportRequestModel,
    GoogleAnalyticsReportingService
)

from webapptitude import testkit as helper
from webapptitude.util import dict_resolve
from webapptitude import oauthkit

from pprint import pprint

import logging
import os
import json


# Provides credentials for Google APIs tests.
secrets = helper.environ_base64_buffer('GOOGLE_API_SECRETS', None)

try:
    secrets = json.loads(secrets.read()) if (secrets is not None) else None
except ValueError:
    secrets = None


def wrap_authorize(method):
    """Ensure that the credentials are present to run the tests..."""
    message = "Requires GOOGLE_API_SECRETS in testing environment."
    q = helper.unittest.skipUnless(isinstance(secrets, dict), message)
    return q(method)


class GoogleAnalyticsReportModelTestCase(helper.TestCase):
    """
    Construct and verify Analytics Reporting API V4 report request objects.

    Specification from Google:
    https://developers.google.com/resources/api-libraries/documentation/analyticsreporting/v4/python/latest/analyticsreporting_v4.reports.html

    These tests produce a deeply nested dictionary, and compare against the
    expected JSON structure Google has documented (as of 2016-06-20).

    """

    init_stubs = True

    # Some constants for simpler validation
    LANDING_PAGE = "ga:landingPagePath"
    PAGE_PATH = "ga:pagePath"
    PAGEVIEWS = "ga:pageviews"
    SESS_DURATION = "ga:avgSessionDuration"
    SESS_PAGEVIEWS = "ga:pageviewsPerSession"
    CITY = "ga:city"
    MEDIUM = "ga:medium"
    SOURCE = "ga:source"
    BLOG_FILTER = '^/blog/'

    @classmethod
    def setUpClass(cls):

        if isinstance(secrets, dict):
            auth1 = oauthkit.json(secrets)
            cls.ga_service = GoogleAnalyticsReportingService(auth1)
        else:
            cls.ga_service = None

        batch = ReportBatch("abc123")   # the (viewId == abc123) for test.
        report = batch.cursor

        batch.add_date_range('2016-04-01', '2016-04-28')
        batch.add_date_range('2016-05-01', '2016-05-28')

        report.add_dimension(cls.SOURCE)
        report.add_metric(cls.SESS_DURATION)

        # all pageviews to the blog
        blog = report.build_dimension_filter(cls.PAGE_PATH, cls.BLOG_FILTER)

        # The report with a pivot (which will also be segmented...)
        report.add_pivot(report.build_pivot_clause(
            [report.build_metric_clause(cls.PAGEVIEWS)],  # pagevews
            [
                report.build_dimension_clause(cls.CITY),  # column: city
                report.build_dimension_clause(cls.PAGE_PATH)  # column: path
            ],
            dim_filters=[
                report.build_dimension_filter_clause(blog)
            ]
        ))

        # The report with a segment.
        report2 = batch.next_report()  # Create a secondary report instance.

        report2.add_metric_filters([
            report.build_metric_filter(cls.PAGEVIEWS, "1",
                                       operator='GREATER_THAN')
        ])

        report2.add_dimension_filters(
            # sessions landing on the blog...
            report.build_dimension_filter_clause(
                report.build_dimension_filter(cls.SOURCE, "google")
            )
        )

        report2.add_dimension(cls.LANDING_PAGE)
        report2.add_metric(cls.SESS_DURATION)
        report2.apply_order(cls.SESS_DURATION, sort_order='DESCENDING')

        # NOTE using function alias only for PEP8.
        dimseg = batch.build_segment_filter_dimension_clause  # shortcut
        metseg = batch.build_segment_filter_metric_clause

        organic = dimseg(cls.MEDIUM, 'EXACT', 'organic')
        # paid = dimseg(cls.MEDIUM, 'EXACT', 'cpc')
        direct = dimseg(cls.MEDIUM, 'EXACT', '(direct)')
        social_sources = ['facebook.com', 'twitter.com']
        social = dimseg(cls.SOURCE, 'IN_LIST', social_sources)
        nonbounce = metseg(cls.PAGEVIEWS, "SESSION", "GREATER_THAN", 1)

        batch.add_segment(
            batch.build_segment(
                "goodmarketing",

                # This session attends only to the organic non-bouncing visits
                sessions=[batch.build_simple_segment([social], [nonbounce])],

                # From users who have multiple marketing touch points...
                users=[batch.build_sequence_segment(

                    # First a social source
                    # batch.build_segment_sequence_step('PRECEDES', [paid]),

                    # Then (eventually) a social source
                    batch.build_segment_sequence_step('IMMEDIATELY_PRECEDES',
                                                      [social]),

                    # Then (immediately) an organic source
                    batch.build_segment_sequence_step('PRECEDES', [direct])
                )]
            ),
            batch.build_segment(
                "all",
                sessions=[batch.build_simple_segment([
                    dimseg(cls.LANDING_PAGE, 'REGEXP', '^/')
                ])]
            )
        )

        # A new batch is necessary because cohorts require a distinct group of
        # dimensions and metrics, and conflict with various other settings above.
        # https://developers.google.com/analytics/devguides/reporting/core/v4/advanced#dimensions
        batch2 = ReportBatch("xyz321")

        batch2.cursor.add_dimension("ga:cohortNthMonth")
        batch2.cursor.add_metric("ga:cohortTotalUsers")

        batch2.add_cohort(
            batch.build_cohort("16Mar", '2016-03-01', '2016-03-31'),
            batch.build_cohort("16April", '2016-04-01', '2016-04-30'),
            batch.build_cohort("16May", '2016-05-01', '2016-05-31')
        )

        cls.batch = batch
        cls.batch2 = batch2
        cls.rendered = batch.to_dict(batch.view_id)
        cls.rendered2 = batch2.to_dict(batch2.view_id)

        return super(GoogleAnalyticsReportModelTestCase, cls).setUpClass()

    def testReportCount(self):
        self.assertEqual(len(self.rendered['reportRequests']), 2)

    def testViewIdentity(self):
        prop = "reportRequests[0].viewId"
        self.assertEqual(dict_resolve(self.rendered, prop), "abc123")

    def testDateRange(self):
        date_ranges = "reportRequests[0].dateRanges"
        date_ranges = dict_resolve(self.rendered, date_ranges)
        # logging.info(repr(self.rendered))
        self.assertEqual(len(date_ranges), 2)
        self.assertEqual(date_ranges[1]['startDate'], '2016-05-01')

    def testZFilterSpecification(self):
        dim = "reportRequests[1].dimensionFilterClauses[0].filters[0]"
        dim = dict_resolve(self.rendered, dim)
        self.assertEqual(dim['dimensionName'], self.SOURCE)
        self.assertEqual(dim['expressions'][0], "google")

        met = "reportRequests[1].metricFilterClauses[0].filters[0]"
        met = dict_resolve(self.rendered, met)
        self.assertEqual(met['operator'], 'GREATER_THAN')
        self.assertEqual(met['metricName'], self.PAGEVIEWS)
        self.assertEqual(met['comparisonValue'], '1')

    def testPivotSpecification(self):
        piv = "reportRequests[0].pivots[0]"
        dim = dict_resolve(self.rendered, piv + 'dimensions[0]')
        met = dict_resolve(self.rendered, piv + 'metrics[0]')
        fil = dict_resolve(self.rendered, piv + 'dimensionFilterClauses[0]')

        self.assertEqual(dim['name'], self.CITY)
        self.assertEqual(met['expression'], self.PAGEVIEWS)
        self.assertEqual(fil['filters'][0]['dimensionName'], self.PAGE_PATH)

    def testSegmentSpecification(self):
        seg = "reportRequests[0].segments[0].dynamicSegment"
        seg = dict_resolve(self.rendered, seg)
        self.assertIn('userSegment', seg)
        self.assertIn('sessionSegment', seg)
        self.assertEqual(seg['name'], 'goodmarketing')

        # logging.info(seg)
        organic = ('sessionSegment.segmentFilters[0].simpleSegment.'
                   'orFiltersForSegment[0]segmentFilterClauses[0].'
                   'dimensionFilter')

        organic = dict_resolve(seg, organic)
        self.assertEqual(organic['dimensionName'], self.SOURCE)

    @wrap_authorize
    # @helper.debug_on(AssertionError, IndexError, TypeError)
    def testQueryGoogleAnalyticsProfileList_integration(self):
        ga = self.ga_service
        profiles = list(ga.profiles)
        has_found = False
        for p in profiles:
            if p.ident[2] == '106132599':
                has_found = True
        self.assertEqual(has_found, True)
        # print repr(profiles)

    @wrap_authorize
    # @helper.debug_on(AssertionError, IndexError, TypeError)
    def testQueryGoogleAnalyticsPivot_integration(self):
        view_id = '106132599'  # Sam's blog
        ga = self.ga_service

        report_result = list(self.batch.fetch(ga, view_id))

        # THe first batch should have two reports.
        self.assertEqual(len(report_result), 2)

        # Assessing the first report of the first batch above.
        # It's expected to have both segments and pivots in play.
        report1 = list(report_result[0].rows)
        dim1, met1, piv1 = report1[0]  # first record/row
        self.assertEqual(dim1[0][0], self.SOURCE)
        self.assertEqual(dim1[1][0], "ga:segment")
        self.assertEqual(dim1[1][1], "all")
        self.assertEqual(met1[0][0], self.SESS_DURATION)

        # A pivot element represents a unique combination of the pivoted
        # attributes. These are expressed as a dictionary.
        self.assertIsInstance(piv1[0][0][0], dict)
        self.assertIn(self.CITY, piv1[0][0][0])
        self.assertIn(self.PAGE_PATH, piv1[0][0][0])

        # Each pivot has its associated metrics (name/value pair)
        self.assertEqual(piv1[0][0][1], self.PAGEVIEWS)  # the name
        self.assertIsInstance(piv1[0][0][2], int)  # the value

        # Assessing the second report of the first batch above.
        # It's expcted to have segments, but not pivots.
        report2 = list(report_result[1].rows)
        dim2, met2, piv2 = report2[0]  # the first record/row
        self.assertEqual(dim2[0][0], self.LANDING_PAGE)  # the first dimension
        self.assertEqual(dim2[1][0], "ga:segment")  # the second segment
        self.assertEqual(dim2[1][1], "all")  # the second segment's name
        self.assertIs(piv2, None)

        # for report in report_result:
        #     pprint(report.base)
        #     pprint(list(report))

    @wrap_authorize
    # @helper.debug_on(AssertionError, IndexError, TypeError)
    def testQueryGoogleAnalyticsCohort_integration(self):
        view_id = '106132599'  # Sam's blog
        ga = self.ga_service
        # pprint(self.rendered2)

        report_result = list(self.batch2.fetch(ga, view_id))

        # The second batch should have only one report.
        self.assertEqual(len(report_result), 1)

        # Assess the first report of the second batch above.
        data = list(report_result[0].rows)  # evalute the iterator

        # Three components: list(dimensions), list(metrics), list(pivots)
        dim1, met1, piv1 = data[0]  # first record/row returned

        self.assertIs(piv1, None)  # this report has no pivots
        self.assertIsInstance(dim1[1], tuple)
        self.assertEqual(dim1[0][0], u'ga:cohortNthMonth')  # 1st dimension
        self.assertEqual(met1[0][0], u'ga:cohortTotalUsers')  # 1st metric

        # for report in report_result:
        #     pprint(report.base)
        #     pprint(list(report))
