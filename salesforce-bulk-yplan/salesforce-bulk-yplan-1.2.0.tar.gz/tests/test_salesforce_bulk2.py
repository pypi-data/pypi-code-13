from __future__ import absolute_import, print_function, unicode_literals

import re
import unittest
import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse  # Py3 compatibility

import pytest
import salesforce_oauth_request

import six
from salesforce_bulk import salesforce_bulk

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


class ResponseStub(object):

    def __init__(self, status):
        self.status = status


class BaseSalesforceTestCase(unittest.TestCase):

    def setUp(self):
        login = salesforce_oauth_request.login(
            username=USERNAME,
            password=PASSWORD,
            token=SECURITY_TOKEN,
            client_id=CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            sandbox=False,  # Developer accounts do not have sandboxes.
        )

        endpoint = urlparse.urlparse(login['endpoint'])
        endpoint = endpoint.hostname

        self.bulk = salesforce_bulk.SalesforceBulk(
            login['access_token'],
            endpoint,
        )
        self.jobs = []

    def tearDown(self):
        if hasattr(self, 'bulk'):
            for job_id in self.jobs:
                print("Closing job: {job_id}".format(job_id=job_id))
                self.bulk.close_job(job_id)


class CheckStatusTestCase(BaseSalesforceTestCase):

    def test_raise_error_no_status_code(self):
        expected_message = salesforce_bulk.IncompleteCredentialsMessage()
        with pytest.raises(salesforce_bulk.BulkApiError) as excinfo:
            self.bulk.raise_error(expected_message)

        assert six.text_type(excinfo.value) == expected_message

    def test_raise_error_with_status_code(self):
        message = salesforce_bulk.IncompleteCredentialsMessage()
        status_code = 999
        with pytest.raises(salesforce_bulk.BulkApiError) as excinfo:
            self.bulk.raise_error(message, status_code)

        expected_message = "[{status_code}] {message}".format(
            status_code=status_code,
            message=message,
        )
        assert six.text_type(excinfo.value) == expected_message

    def test_check_status_success(self):
        response = ResponseStub(status=200)

        self.bulk.check_status(response, "Nothing should happen.")

    def test_check_status_client_error(self):
        response = ResponseStub(status=404)

        with pytest.raises(salesforce_bulk.BulkApiError) as excinfo:
            self.bulk.check_status(response, "Not Found")

        expected_message = "[{status_code}] {message}".format(
            status_code=response.status,
            message=salesforce_bulk.HttpErrorMessage(message="Not Found"),
        )

        assert six.text_type(excinfo.value) == expected_message


class JobDocsTestCase(BaseSalesforceTestCase):

    def test_create_job_doc(self):
        job_doc = self.bulk.create_job_doc(
            object_name="Campaign",
            operation="insert",
        )

        expected_doc = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<jobInfo xmlns=\"http://www.force.com/2009/06/asyncapi/dataload\">"
            "<operation>{operation}</operation><object>{object_name}</object>"
            "<contentType>CSV</contentType></jobInfo>"
        ).format(
            object_name="Campaign",
            operation="insert",
        ).lower()

        assert job_doc.decode('utf-8').lower() == expected_doc

    def test_create_close_job_doc(self):
        job_doc = self.bulk.create_close_job_doc()

        expected_doc = (
            "<?xml version=\'1.0\' encoding=\'utf-8\'?>\n"
            "<jobInfo xmlns=\"http://www.force.com/2009/06/asyncapi/dataload\">"
            "<state>Closed</state></jobInfo>"
        ).lower()
        assert job_doc.decode('utf-8').lower() == expected_doc

    def test_create_abort_job_doc(self):
        job_doc = self.bulk.create_abort_job_doc()

        expected_doc = (
            "<?xml version=\'1.0\' encoding=\'utf-8\'?>\n"
            "<jobInfo xmlns=\"http://www.force.com/2009/06/asyncapi/dataload\">"
            "<state>Aborted</state></jobInfo>"
        ).lower()
        assert job_doc.decode('utf-8').lower() == expected_doc


class JobControlTestCase(BaseSalesforceTestCase):

    def test_create_query_job(self):
        job_id = self.bulk.create_query_job("Campaign")
        self.jobs.append(job_id)

        assert job_id is not None

    def test_create_insert_job(self):
        job_id = self.bulk.create_insert_job("Campaign")
        self.jobs.append(job_id)

        assert job_id is not None

    def test_create_upsert_job(self):
        job_id = self.bulk.create_upsert_job("Campaign", "Name")
        self.jobs.append(job_id)

        assert job_id is not None

    def test_create_delete_job(self):
        job_id = self.bulk.create_delete_job("Campaign")
        self.jobs.append(job_id)

        assert job_id is not None

    def test_close_query_job(self):
        job_id = self.bulk.create_query_job("Campaign")

        assert job_id is not None

        self.bulk.close_job(job_id)

    def test_close_insert_job(self):
        job_id = self.bulk.create_insert_job("Campaign")

        assert job_id is not None

        self.bulk.close_job(job_id)

    def test_close_upsert_job(self):
        job_id = self.bulk.create_upsert_job("Campaign", "Name")

        assert job_id is not None

        self.bulk.close_job(job_id)

    def test_close_delete_job(self):
        job_id = self.bulk.create_delete_job("Campaign")

        assert job_id is not None

        self.bulk.close_job(job_id)

    def test_abort_job(self):
        job_id = self.bulk.create_delete_job("Campaign")

        assert job_id is not None

        self.bulk.abort_job(job_id)


class QueryTestCase(BaseSalesforceTestCase):

    def test_without_job_id(self):
        batch_id = self.bulk.query(None, "SELECT Id, Name FROM Account")

        assert batch_id is not None
        assert batch_id in self.bulk.batches

        self.bulk.close_job(self.bulk.batches[batch_id])

    def test_with_job_id(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        assert batch_id is not None
        assert batch_id in self.bulk.batches
        assert job_id == self.bulk.batches[batch_id]

        self.bulk.close_job(job_id)


class SplitCsvTestCase(BaseSalesforceTestCase):

    def test_empty_string(self):
        assert self.bulk.split_csv("", 10) == []

    def test_header_only(self):
        csv_content = "\n".join([
            "Id,Name",
        ])
        assert self.bulk.split_csv(csv_content, 10) == [csv_content]

    def test_one_batch(self):
        csv_content = "\n".join([
            "Id,Name",
            "SOABCDEFGH,Test",
        ])
        assert self.bulk.split_csv(csv_content, 10) == [csv_content]

    def test_two_batches(self):
        csv_content = "\n".join([
            "Id,Name"
        ] + [
            "SOABCDEFGH,Test",
        ] * 5)
        expected_batches = [
            ("\n".join(["Id,Name"] + ["SOABCDEFGH,Test"] * 2) + "\n"),
            ("\n".join(["Id,Name"] + ["SOABCDEFGH,Test"] * 3)),
        ]
        assert self.bulk.split_csv(csv_content, 3) == expected_batches


class BulkOperationsTestCase(BaseSalesforceTestCase):

    def test_upload_delete(self):
        job_id = self.bulk.create_insert_job("Account")
        csv_content = "\n".join([
            "Name",
            "test_salesforce_bulk.BulkOperationsTestCase.test_upload_delete",
        ])
        batch_ids = self.bulk.bulk_csv_upload(job_id, csv_content)

        assert len(batch_ids) == 1

        batch_id = batch_ids[0]

        self.bulk.wait_for_batch(job_id, batch_id)

        records = []
        def callback(rows, total, line):
            records.extend(rows)

        assert self.bulk.get_upload_results(
            job_id,
            batch_id,
            callback=callback,
        )

        assert len(records) == 2
        assert all(bool(r.error) is False for r in records[1:])
        assert all(r.success == 'true' for r in records[1:])
        assert all(r.created == 'true' for r in records[1:])

        object_id = records[1].id

        assert object_id

        self.bulk.close_job(job_id)

        job_id = self.bulk.create_delete_job("Account")
        csv_content = "\n".join(["Id", object_id])

        batch_ids = self.bulk.bulk_delete(
            job_id,
            "Account",
            "Id = '{object_id}'".format(object_id=object_id),
        )

        assert len(batch_ids) == 1

        batch_id = batch_ids[0]

        self.bulk.wait_for_batch(job_id, batch_id)
        status = self.bulk.batch_state(job_id, batch_id, reload=True)

        assert status == "Completed"

        self.bulk.close_job(job_id)

    def test_post_bulk_batch(self):
        csv_content = [
            "Name\n",
            "test_salesforce_bulk.BulkOperationsTestCase.test_post_bulk_batch",
        ]

        job_id = self.bulk.create_insert_job("Account", contentType='CSV')
        batch_id = self.bulk.post_bulk_batch(
            job_id,
            iter(csv_content),
        )

        self.bulk.wait_for_batch(job_id, batch_id)
        status = self.bulk.batch_state(job_id, batch_id, reload=True)

        assert status == "Completed"

        self.bulk.close_job(job_id)


class LookupJobIdTestCase(BaseSalesforceTestCase):

    def test_invalid_job(self):
        with pytest.raises(Exception) as excinfo:
            self.bulk.lookup_job_id(batch_id=9001)

        expected_message = "Batch id '9001' is unknown, can't retrieve job_id."
        assert six.text_type(excinfo.value) == expected_message


class JobStatusTestCase(BaseSalesforceTestCase):

    def test_without_ids(self):
        with pytest.raises(Exception) as excinfo:
            self.bulk.job_status()

        expected_message = "Batch id 'None' is unknown, can't retrieve job_id."
        assert six.text_type(excinfo.value) == expected_message

    def test_with_job_id(self):
        job_id = self.bulk.create_query_job("Account")

        assert job_id is not None

        status = self.bulk.job_status(job_id=job_id)

        assert status is not None
        assert type(status) == dict

        self.bulk.close_job(job_id)

    def test_with_batch_id(self):
        batch_id = self.bulk.query(None, "SELECT Id, Name FROM Account")

        assert batch_id is not None

        status = self.bulk.job_status(batch_id=batch_id)

        assert status is not None
        assert type(status) == dict

        self.bulk.close_job(self.bulk.batches[batch_id])

    def test_job_state(self):
        job_id = self.bulk.create_query_job("Account")

        assert job_id is not None

        status = self.bulk.job_state(job_id)

        assert status == "Open"

        self.bulk.close_job(job_id)

        status = self.bulk.job_state(job_id)

        assert status == "Closed"


class BatchStatusTestCase(BaseSalesforceTestCase):

    def test_cached_status(self):
        self.bulk.batch_statuses[9001] = "cached"

        assert self.bulk.batch_status(batch_id=9001, reload=False) == "cached"

    def test_with_job_id(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        status = self.bulk.batch_status(job_id=job_id, batch_id=batch_id)

        assert status is not None
        assert type(status) == dict

        self.bulk.close_job(job_id)

    def test_without_job_id(self):
        batch_id = self.bulk.query(None, "SELECT Id, Name FROM Account")

        status = self.bulk.batch_status(batch_id=batch_id)

        assert status is not None
        assert type(status) == dict

        self.bulk.close_job(self.bulk.batches[batch_id])

    def test_batch_state(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        status = self.bulk.batch_state(job_id, batch_id, reload=False)

        self.bulk.wait_for_batch(job_id, batch_id)
        assert status == "Completed"

        self.bulk.close_job(job_id)

        status = self.bulk.batch_state(job_id, batch_id, reload=False)

        assert status == "Completed"

        status = self.bulk.batch_state(job_id, batch_id, reload=True)

        assert status == "Completed"


class BatchDoneTestCase(BaseSalesforceTestCase):

    def test_completed(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        state = self.bulk.batch_state(job_id, batch_id, reload=True)
        counter = 0
        while state == 'Queued':
            assert counter < 10
            state = self.bulk.batch_state(job_id, batch_id, reload=True)
            counter += 1

        assert self.bulk.is_batch_done(job_id, batch_id)

        self.bulk.close_job(job_id)


class GetBatchResultsTestCase(BaseSalesforceTestCase):

    def test_result_ids(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        self.bulk.wait_for_batch(job_id, batch_id)
        result = self.bulk.get_batch_result_ids(batch_id, job_id)

        assert result is not None

        self.bulk.close_job(job_id)

    def test_results(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        self.bulk.wait_for_batch(job_id, batch_id)
        result = list(self.bulk.get_all_results_for_batch(batch_id, job_id))

        assert result is not None

        result = list(result[0])

        assert '"Id","Name"' in result
        assert len(result) > 1

        self.bulk.close_job(job_id)

    def test_results_parse_csv(self):
        job_id = self.bulk.create_query_job("Account")
        batch_id = self.bulk.query(job_id, "SELECT Id, Name FROM Account")

        self.bulk.wait_for_batch(job_id, batch_id)
        result = list(self.bulk.get_all_results_for_batch(batch_id, job_id, parse_csv=True))

        assert result is not None

        result = list(result[0])

        assert result[0] == ["Id", "Name"]
        assert all(len(row) == 2 for row in result)

        self.bulk.close_job(job_id)
