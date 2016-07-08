#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# DOCS
# =============================================================================

"""Basic structures and functionality for running tests on otree

"""

# =============================================================================
# IMPORTS
# =============================================================================

import logging
import contextlib
import collections
import random
import mock

from six import StringIO
from six.moves import zip_longest

from django.db.migrations.loader import MigrationLoader
from django import test
from django.test import runner
from unittest import TestSuite

from otree import constants_internal, session, common_internal
from otree.test.client import ParticipantBot


import coverage

# =============================================================================
# CONSTANTS
# =============================================================================

COVERAGE_MODELS = ['models', 'tests', 'views']

MAX_ATTEMPTS = 100


# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# PENDING LIST
# =============================================================================

class PendingBuffer(object):

    def __init__(self):
        self.storage = collections.OrderedDict()

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self.storage)

    def __bool__(self):
        return bool(self.storage)

    # For Python 2 compatibiliy.
    __nonzero__ = __bool__

    def __iter__(self):
        for k, v in list(self.storage.items()):
            yield k, v
            if k in self.storage:
                self.storage[k] += 1

    def add(self, submit):
        if submit in self.storage:
            raise ValueError("Submit already in pending list")
        self.storage[submit] = 1

    def remove(self, submit):
        del self.storage[submit]

    def is_blocked(self, submit):
        return submit.bot in [s.bot for s in self.storage.keys()]


# =============================================================================
# TEST CASE
# =============================================================================

class OTreeExperimentFunctionTest(test.TransactionTestCase):

    def __init__(self, session_name, preserve_data):
        super(OTreeExperimentFunctionTest, self).__init__()
        self.session_name = session_name
        self.preserve_data = preserve_data
        self._data = None

    def __repr__(self):
        hid = hex(id(self))
        return "<{} '{}'>".format(type(self).__name__, self.session_name, hid)

    def __str__(self):
        return "ExperimentTest for session '{}'".format(self.session_name)

    def zip_submits(self, bots):
        bots = list(bots)
        random.shuffle(bots)
        submits = [b.submits for b in bots]
        return list(zip_longest(*submits))

    def tearDown(self):
        if self.preserve_data:
            logger.info(
                "Recolecting data for session '{}'".format(self.session_name))
            buff = StringIO()
            common_internal.export_data(buff, self.session_name)
            self._data = buff.getvalue()

    def get_data(self):
        return self._data

    def runTest(self):
        logger.info("Creating '{}' session".format(self.session_name))

        sssn = session.create_session(
            session_config_name=self.session_name,
            special_category=constants_internal.session_special_category_bots)
        sssn.label = '{} [bots]'.format(self.session_name)
        sssn.save()

        # since players are assigned to groups in a background thread,
        # we need to wait for that to complete.
        logger.info("Adding bots on session '{}'".format(self.session_name))

        msg = "'GET' over first page of all '{}' participants"
        logger.info(msg.format(self.session_name))

        participant_bots = []
        for participant in sssn.get_participants():
            participant_bot = ParticipantBot(participant)
            participant_bots.append(participant_bot)
            participant_bot.start()

        submit_groups = self.zip_submits(participant_bots)
        pending = PendingBuffer()
        while pending or submit_groups:

            seen_pending_bots = set()
            for submit, attempts in pending:
                if attempts > MAX_ATTEMPTS:
                    msg = "Max attepts reached in  submit '{}'"
                    raise AssertionError(msg.format(submit))
                if submit.bot not in seen_pending_bots and submit.execute():
                    pending.remove(submit)
                else:
                    seen_pending_bots.add(submit.bot)

            group = submit_groups.pop(0) if submit_groups else ()
            for submit in group:
                if submit is None:
                    continue
                if pending.is_blocked(submit) or not submit.execute():
                    pending.add(submit)

        logger.info("Stopping bots")
        for bot in participant_bots:
            bot.stop()


# =============================================================================
# RUNNER
# =============================================================================

class OTreeExperimentTestSuite(TestSuite):
    def _removeTestAtIndex(self, index):
        # In Python 3.4 and above, is the TestSuite clearing all references to
        # the test cases after the suite has finished. That way, the
        # ``OTreeExperimentTestRunner.suite_result`` cannot retrieve the data
        # in order to prepare it for CSV test data export.

        # We overwrite this function in order to keep the testcase instances
        # around.
        pass


class OTreeExperimentTestRunner(runner.DiscoverRunner):
    test_suite = OTreeExperimentTestSuite

    def build_suite(self, session_names, extra_tests, preserve_data, **kwargs):
        suite = self.test_suite()
        for session_name in session_names:
            case = OTreeExperimentFunctionTest(session_name, preserve_data)
            suite.addTest(case)
        return suite

    def suite_result(self, suite, result, *args, **kwargs):
        failures = super(OTreeExperimentTestRunner, self).suite_result(
            suite, result, *args, **kwargs)
        data = {case.session_name: case.get_data() for case in suite}
        return failures, data

    def run_tests(self, test_labels, extra_tests=None,
                  preserve_data=False, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests, preserve_data)
        # same hack as in resetdb code
        # because this method uses the serializer
        # it breaks if the app has migrations but they aren't up to date
        with mock.patch.object(
                MigrationLoader,
                'migrations_module',
                return_value='migrations nonexistent hack'
        ):
            old_config = self.setup_databases()
        result = self.run_suite(suite)
        failures, data = self.suite_result(suite, result)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return failures, data


# =============================================================================
# COVERAGE CONTEXT
# =============================================================================

@contextlib.contextmanager
def covering(session_names=None):
    package_names = set()
    for app_label in session.app_labels_from_sessions(session_names):
        for module_name in COVERAGE_MODELS:
            module = '{}.{}'.format(app_label, module_name)
            package_names.add(module)

    cov = coverage.coverage(source=package_names)
    cov.start()
    try:
        yield cov
    finally:
        cov.stop()
