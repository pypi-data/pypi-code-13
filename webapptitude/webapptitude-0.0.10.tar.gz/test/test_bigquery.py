"""BigQuery API integration tests."""

from webapptitude import bigquery
from webapptitude import testkit as helper
from webapptitude import oauthkit

from contextlib import contextmanager
from datetime import datetime, timedelta

import os
import time
import random
import string
import json

# Provides credentials for Google APIs tests.
secrets = helper.environ_base64_buffer('GOOGLE_API_SECRETS', None)
try:
    secrets = json.loads(secrets.read()) if (secrets is not None) else None
except ValueError:
    secrets = None

_errors = (AssertionError, IndexError, TypeError, AttributeError,
           bigquery.googleapi.HttpError)

# TODO: migrate to own dataset (stop using measurelink.)

# When True, SKIP_ASYNC will prevent some tests that run long and slow.
SKIP_ASYNC = bool(int(os.environ.get('SKIP_ASYNC', 0)))
DO_BIGQUERY_TEST = bool(int(os.environ.get('TEST_BIGQUERY', 0)))

def _flatten(deeplist):
    """Flatten some nested lists."""
    return [i for l in deeplist for i in l]


def random_id(size=10, chars=(string.ascii_uppercase + string.digits)):
    """Generate a unique ID (for each test run)."""
    return ''.join(random.choice(chars) for x in range(0, size))


def wrap_authorize(method):
    """Ensure that the credentials are present to run the tests..."""
    message = "Requires GOOGLE_API_SECRETS in testing environment."
    q = helper.unittest.skipUnless(isinstance(secrets, dict), message)
    return q(method)


@helper.unittest.skipUnless(DO_BIGQUERY_TEST, "BigQuery tests disabled.")
class BigQueryTestKit(helper.TestCase):

    # A super-simple query to run after populating data...
    sql_template = ('SELECT COUNT(*) as Q FROM [{dataset}.{table}];')

    @classmethod
    # @helper.debug_on(AssertionError, IndexError, TypeError, AttributeError)
    def setUpClass(cls):

        if isinstance(secrets, dict):
            auth1 = oauthkit.json(secrets)
            cls.service = bigquery.BigQueryService(auth1)

        cls.dataset_id = 'test_dataset_' + random_id(5)
        return super(BigQueryTestKit, cls).setUpClass()

    @classmethod
    def gen_dataset_id(self, size=5):
        return 'test_dataset_%s' % (random_id(size),)

    @property
    def cur_project(self):
        """Accesssor to the first project available to the test account."""
        return list(self.service.projects)[0]

    @contextmanager
    def basedata(self):
        """
        Prepare the underlying data for each test.

        This exercises some functionality that should be independently tested
        as well. It's therefore treated as a utility of this test class, and
        will not be loaded by default in the TestCase.setUp method.

        In effect this is providing a test fixture inside a real BigQuery
        environment, and then cleaning it up once the test completes.
        """

        project_id, project_name, project = self.cur_project

        hour = (3600 * 1000)
        dataset_id = self.gen_dataset_id()
        dataset = project.create_dataset(dataset_id,
                                         "Dataset for test",
                                         tables_expire=hour)

        schema = dict(
            timestamp=('TIMESTAMP', 'REQUIRED', 'My timestamp field.'),
            counter=('INTEGER', None, None),
            item_name=('STRING', 'REQUIRED', "The name of this item.")
        )

        table_id = 'table_test_%s' % (random_id(5),)
        table = dataset.prepare_table(table_id, "Test table", schema)

        tomorrow = datetime.utcnow() + timedelta(days=1)

        table.insert(  # load a few records to query
            dict(timestamp="NOW", counter=7, item_name="pizza"),
            dict(timestamp=tomorrow, counter=1, item_name="milkshake")
        )

        try:
            yield dict(
                datasetId=dataset_id,
                tableId=table_id,
                dataset=dataset,
                table=table,
                sql=(self.sql_template.format(dataset=dataset_id,
                                              table=table_id))
            )
        finally:
            dataset.delete()

    @wrap_authorize
    # @helper.debug_on(AssertionError, IndexError, TypeError)
    def test0ListProjects(self):
        projects = list(self.service.projects)
        self.assertTrue(len(projects) > 0)

        project_id = projects[0][0]
        project = self.service.get_project(project_id)
        self.assertIsInstance(project, bigquery.Project)
        # print repr(projects)

    @wrap_authorize
    def test0Dataset_SetupTeardown(self):
        """Constructs and then destroys a dataset."""
        pid, pname, project = list(self.service.projects)[0]

        dataset_id = self.gen_dataset_id()
        dataset = project.create_dataset(dataset_id,
                                         "Dataset for Test",
                                         tables_expire=3600 * 1000)

        self.assertTrue(project.dataset_exists(dataset_id))
        self.assertIsInstance(project.get_dataset(dataset_id), bigquery.Dataset)

        dataset.delete()
        self.assertFalse(project.dataset_exists(dataset_id))

    @wrap_authorize
    # @helper.debug_on(*_errors)
    def testConstructProject_ListDatasetsTables(self):

        # Wrap this in context, to we can be sure that a table exists.
        with self.basedata() as data:
            project_id, project_name, project = self.cur_project

            datasets = list(project.datasets)
            self.assertTrue(len(datasets) > 0)

            tables = _flatten([d.tables for (i, n, d) in datasets])
            self.assertTrue(len(tables) > 0)

    @wrap_authorize
    @helper.unittest.skipUnless(not SKIP_ASYNC, "ASYNC queries take too long.")
    # @helper.debug_on(*_errors)
    def testDatasetQuery_1async_integration(self):
        """Perform an asynchronous query, and poll for it..."""
        with self.basedata() as data:
            project_id, project_name, project = self.cur_project
            sql = data.get('sql')
            job = project.query(sql, async=True)
            while 1:
                self.logger.info('Waiting on results...')
                time.sleep(5)
                try:
                    results = list(job.results)
                    break
                except bigquery.JobNotReady:
                    continue
            self.assertEqual(len(results), 1)

    @wrap_authorize
    # @helper.debug_on(*_errors)
    def testDatasetQuery_0sync_integration(self):

        with self.basedata() as data:
            project_id, project_name, project = self.cur_project
            sql = data.get('sql')
            results = list(project.query(sql, async=False))
            self.assertEqual(len(results), 1)

    @wrap_authorize
    # @helper.debug_on(*_errors)
    def testDataset_buildTable(self):
        pid, pname, project = self.cur_project

        with self.basedata() as data:
            dataset = data.get('dataset')

            result = dataset.prepare_table(
                "test_table_id_8973", "My Test Table",
                dict(
                    timestamp=('TIMESTAMP', 'REQUIRED', 'My timestamp field.'),
                    counter=('INTEGER', None, None),
                    item_name=('STRING', 'REQUIRED', "The name of this item.")
                )
            )

            self.assertIsInstance(result, bigquery.Table)
            self.assertIn("test_table_id_8973", result.table_id)
            self.assertTrue(dataset.table_exists("test_table_id_8973"))
            table = dataset.get_table("test_table_id_8973")
            self.assertIsInstance(table, bigquery.Table)

    @wrap_authorize
    def testCreateView(self):
        with self.basedata() as data:
            project_id, project_name, project = self.cur_project
            dataset = data.get('dataset')
            dataset_id = data.get('datasetId')
            result = dataset.prepare_view(
                "test_view", "The test view.",
                data.get('sql')
            )
            self.assertIsInstance(result, bigquery.Table)

            sql = "SELECT * FROM [%s.test_view]" % (dataset_id)
            query = list(project.query(sql))
            self.assertEqual(query[0]['Q'], 2)


