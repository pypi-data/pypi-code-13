import time
import unittest
from unittest import TextTestRunner, TestProgram, TextTestResult, loader

from test_listener import TestListener

from python_agent.test_listener import config


class SealightsTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(SealightsTestResult, self).__init__(stream, descriptions, verbosity)
        self.test_listener = TestListener(config.customer_id, config.app_name, config.build, config.branch, config.env)

    def startTestRun(self):
        self.test_listener.start()
        super(SealightsTestResult, self).startTestRun()

    def stopTestRun(self):
        self.test_listener.stop()
        super(SealightsTestResult, self).stopTestRun()

    def startTest(self, test):
        test.start_time = time.time()
        self.test_listener.start_test(test.id())
        super(SealightsTestResult, self).startTest(test)

    def stopTest(self, test):
        test.end_time = time.time()
        test.duration = test.end_time - test.start_time
        self.test_listener.passed_test(test.id(), test.duration)
        super(SealightsTestResult, self).stopTest(test)

    def addError(self, test, err):
        test.end_time = time.time()
        test.duration = test.end_time - test.start_time
        self.test_listener.failed_test(test.id(), test.duration)
        super(SealightsTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        test.end_time = time.time()
        test.duration = test.end_time - test.start_time
        self.test_listener.failed_test(test.id(), test.duration)
        super(SealightsTestResult, self).addFailure(test, err)

    def addSkip(self, test, reason):
        test.end_time = time.time()
        test.duration = test.end_time - test.start_time
        self.test_listener.skipped_test(test.id(), test.duration)
        super(SealightsTestResult, self).addSkip(test, reason)


class SealightsTextTestRunner(TextTestRunner):
    resultclass = SealightsTestResult


class SealightsTestProgram(TestProgram):

    def __init__(self, module='__main__', defaultTest=None, argv=None,
                 testRunner=None, testLoader=loader.defaultTestLoader,
                 exit=True, verbosity=1, failfast=None, catchbreak=None,
                 buffer=None):

        super(SealightsTestProgram, self).__init__(
            module=module, defaultTest=defaultTest, argv=argv,
            testRunner=SealightsTextTestRunner, testLoader=testLoader,
            exit=exit, verbosity=verbosity, failfast=failfast,
            catchbreak=catchbreak, buffer=buffer
        )


unittest.main = SealightsTestProgram
