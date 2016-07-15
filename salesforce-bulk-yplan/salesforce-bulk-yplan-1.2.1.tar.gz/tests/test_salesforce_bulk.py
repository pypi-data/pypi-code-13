import re
import unittest
import os

import salesforce_oauth_request

from salesforce_bulk import SalesforceBulk

# NOTE(JS): I'm preserving this file for general reference, until I
# write new tests in `test_salesforce_bulk2.py`.
__test__ = False

USERNAME = None
PASSWORD = None
SECURITY_TOKEN = None
CONSUMER_KEY = None
CONSUMER_SECRET = None


def setup_module(module):
    global USERNAME, PASSWORD, SECURITY_TOKEN, CONSUMER_KEY, CONSUMER_SECRET

    # See `.travis.yml` on how this is set up.
    USERNAME = os.environ.get('SALESFORCE_USERNAME')
    PASSWORD = os.environ.get('SALESFORCE_PASSWORD')
    SECURITY_TOKEN = os.environ.get('SALESFORCE_SECURITY_TOKEN')
    CONSUMER_KEY = os.environ.get('SALESFORCE_CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('SALESFORCE_CONSUMER_SECRET')

    environment_ready = USERNAME and PASSWORD and SECURITY_TOKEN and CONSUMER_KEY and CONSUMER_SECRET
    assert environment_ready, ("Make sure SALESFORCE_* environment variables pointing to "
                               "developer account are set. Check the test suite to find out more.")

class SalesforceBulkTestCase(unittest.TestCase):

    def setUp(self):
        login = salesforce_oauth_request.login(
            username=USERNAME,
            password=PASSWORD,
            token=SECURITY_TOKEN,
            client_id=CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            cache_session=False,
            sandbox=True,
        )

        self.bulk = SalesforceBulk(login['access_token'], login['endpoint'])
        self.jobs = []

    def tearDown(self):
        if hasattr(self, 'bulk'):
            for job_id in self.jobs:
                print "Closing job: %s" % job_id
                self.bulk.close_job(job_id)

    def test_raw_query(self):
        job_id = self.bulk.create_query_job("Contact")
        self.jobs.append(job_id)
        self.assertIsNotNone(re.match("\w+", job_id))

        batch_id = self.bulk.query(job_id, "Select Id,Name,Email from Contact Limit 1000")
        self.assertIsNotNone(re.match("\w+", batch_id))

        while not self.bulk.is_batch_done(job_id, batch_id):
            print "Job not done yet..."
            print self.bulk.batch_status(job_id, batch_id)
            time.sleep(2)

        self.results = ""
        def save_results(tfile, **kwargs):
            print "in save results"
            self.results = tfile.read()

        flag = self.bulk.get_batch_results(job_id, batch_id, callback = save_results)
        self.assertTrue(flag)
        self.assertTrue(len(self.results) > 0)
        self.assertIn('"', self.results)


    def test_csv_query(self):
        job_id = self.bulk.create_query_job("Account")
        self.jobs.append(job_id)
        self.assertIsNotNone(re.match("\w+", job_id))

        batch_id = self.bulk.query(job_id, "Select Id,Name,Description from Account Limit 10000")
        self.assertIsNotNone(re.match("\w+", batch_id))
        self.bulk.wait_for_batch(job_id, batch_id, timeout=120)

        self.results = None
        def save_results1(rows, **kwargs):
            self.results = rows

        flag = self.bulk.get_batch_results(job_id, batch_id, callback = save_results1, parse_csv=True)
        self.assertTrue(flag)
        results = self.results
        self.assertTrue(len(results) > 0)
        self.assertTrue(isinstance(results,list))
        self.assertEqual(results[0], ['Id','Name','Description'])
        self.assertTrue(len(results) > 3)

        self.results = None
        self.callback_count = 0
        def save_results2(rows, **kwargs):
            self.results = rows
            print rows
            self.callback_count += 1

        batch = len(results) / 3
        self.callback_count = 0
        flag = self.bulk.get_batch_results(job_id, batch_id, callback = save_results2, parse_csv=True, batch_size=batch)
        self.assertTrue(self.callback_count >= 3)


    def test_csv_upload(self):
        job_id = self.bulk.create_insert_job("Contact")
        self.jobs.append(job_id)
        self.assertIsNotNone(re.match("\w+", job_id))

        batch_ids = []
        content = open("example.csv").read()
        for i in range(5):
            batch_id = self.bulk.query(job_id, content)
            self.assertIsNotNone(re.match("\w+", batch_id))
            batch_ids.append(batch_id)

        for batch_id in batch_ids:
            self.bulk.wait_for_batch(job_id, batch_id, timeout=120)

        self.results = None
        def save_results1(rows, failed, remaining):
            self.results = rows

        for batch_id in batch_ids:
            flag = self.bulk.get_upload_results(job_id, batch_id, callback = save_results1)
            self.assertTrue(flag)
            results = self.results
            self.assertTrue(len(results) > 0)
            self.assertTrue(isinstance(results,list))
            self.assertEqual(results[0], UploadResult('Id','Success','Created','Error'))
            self.assertEqual(len(results), 3)

        self.results = None
        self.callback_count = 0
        def save_results2(rows, failed, remaining):
            self.results = rows
            self.callback_count += 1

        batch = len(results) / 3
        self.callback_count = 0
        flag = self.bulk.get_upload_results(job_id, batch_id, callback = save_results2, batch_size=batch)
        self.assertTrue(self.callback_count >= 3)
