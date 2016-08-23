import logging
import urllib
import sys
import time
import unittest
from unittest import TextTestRunner, TestProgram, TextTestResult, loader
from unittest import registerResult
from unittest.main import USAGE_AS_MAIN

from python_agent.test_listener import TestListener
from python_agent.test_listener import config
from python_agent.test_listener.integrations import unittest_parser

__unittest = True

log = logging.getLogger(__name__)


class SealightsTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(SealightsTestResult, self).__init__(stream, descriptions, verbosity)
        self.test_listener = TestListener(config.app["customer_id"], config.app["app_name"], config.app["build"],
                                          config.app["branch"], config.app["env"], config.app["server"])

    def startTestRun(self):
        try:
            self.test_listener.start()
        except Exception as e:
            log.exception("failed sending execution start. error: %s" % str(e))
        super(SealightsTestResult, self).startTestRun()

    def stopTestRun(self):
        try:
            self.test_listener.stop()
        except Exception as e:
            log.exception("failed sending execution end. error: %s" % str(e))
        super(SealightsTestResult, self).stopTestRun()

    def startTest(self, test):
        try:
            test.start_time = time.time()
            self.test_listener.start_test(urllib.pathname2url(test.id()))
        except Exception as e:
            log.exception("failed sending test start. error: %s" % str(e))
        super(SealightsTestResult, self).startTest(test)

    def stopTest(self, test):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.test_listener.passed_test(urllib.pathname2url(test.id()), test.duration)
        except Exception as e:
            log.exception("failed sending test end. error: %s" % str(e))
        super(SealightsTestResult, self).stopTest(test)

    def addError(self, test, err):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.test_listener.failed_test(urllib.pathname2url(test.id()), test.duration)
        except Exception as e:
            log.exception("failed sending test failed. error: %s" % str(e))
        super(SealightsTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.test_listener.failed_test(urllib.pathname2url(test.id()), test.duration)
        except Exception as e:
            log.exception("failed sending test failed. error: %s" % str(e))
        super(SealightsTestResult, self).addFailure(test, err)

    def addSkip(self, test, reason):
        try:
            test.end_time = time.time()
            test.duration = test.end_time - test.start_time
            self.test_listener.skipped_test(urllib.pathname2url(test.id()), test.duration)
        except Exception as e:
            log.exception("failed sending test skipped. error: %s" % str(e))
        super(SealightsTestResult, self).addSkip(test, reason)


class SealightsTextTestRunner(TextTestRunner):
    resultclass = SealightsTestResult

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None and test._tests:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None and test._tests:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result


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


def main():
    argv = []
    try:
        unittest_parser.add_options()
        args, argv = unittest_parser.parse(unittest_parser.global_parser)
    except SystemExit as e:
        unittest_parser.global_parser._print_message("\n======================== Python unittest Options ========================\n")
        unittest_parser.global_parser.exit(status=getattr(e, "code", "2"), message=USAGE_AS_MAIN)
    SealightsTestProgram.USAGE = USAGE_AS_MAIN
    unittest.main(module=None, argv=[sys.argv[0]] + argv)


if __name__ == '__main__':
    main()
