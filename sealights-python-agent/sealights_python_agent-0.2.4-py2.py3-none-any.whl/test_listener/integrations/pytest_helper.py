import urllib
import logging
import logging.config
import operator
from collections import defaultdict

from _pytest.hookspec import hookspec

from python_agent.test_listener import TestListener, config as conf
from python_agent.test_listener.utils import validate_server, validate_server_api, config_logging
from python_agent.utils.autoupgrade import AutoUpgrade

log = logging.getLogger(__name__)


class SealightsPlugin(object):
    def __init__(self):
        self.test_listener = TestListener(conf.app["customer_id"], conf.app["app_name"], conf.app["build"],
                                          conf.app["branch"], conf.app["env"], conf.app["server"])
        self.test_status = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))

    def pytest_sessionstart(self, session):
        try:
            self.test_listener.start()
        except Exception as e:
            log.exception("failed sending execution start. error: %s" % str(e))

    def pytest_sessionfinish(self, session, exitstatus):
        try:
            self.test_listener.stop()
        except Exception as e:
            log.exception("failed sending execution end. error: %s" % str(e))

    def pytest_runtest_logstart(self, nodeid, location):
        try:
            self.test_listener.start_test(urllib.pathname2url(nodeid))
        except Exception as e:
            log.exception("failed sending test start. error: %s" % str(e))

    @hookspec(firstresult=True)
    def pytest_report_teststatus(self, report):
        try:
            self.test_status[report.nodeid]["passed"][report.when] = report.passed
            self.test_status[report.nodeid]["skipped"][report.when] = report.skipped
            self.test_status[report.nodeid]["failed"][report.when] = report.failed
            if report.when == "teardown":
                test = self.test_status[report.nodeid]
                passed = reduce(operator.and_, test["passed"].values())
                skipped = reduce(operator.or_, test["skipped"].values())
                failed = reduce(operator.or_, test["failed"].values())
                if passed:
                    self.test_listener.passed_test(urllib.pathname2url(report.nodeid), report.duration)
                elif skipped:
                    self.test_listener.skipped_test(urllib.pathname2url(report.nodeid), report.duration)
                elif failed:
                    self.test_listener.failed_test(urllib.pathname2url(report.nodeid), report.duration)
        except Exception as e:
            log.exception("failed sending test end, skip or failed. error: %s" % str(e))

    def pytest_internalerror(excrepr, excinfo):
        log.exception("sealights plugin internal error. exception: %s. excinfo: %s" % (excrepr, excinfo))

    def pytest_exception_interact(node, call, report):
        log.exception("sealights plugin exception. call: %s. report: %s" % (call, report))


def pytest_addoption(parser):
    parser.addoption("--customer_id", required=True, help="An id representing the client")
    parser.addoption("--app_name", required=True, help="The name of the application")
    parser.addoption("--server", type=validate_server, required=True, help="Sealights Server. Must be of the form: http://<server>/api")
    parser.addoption("--build", default="1", help="The build number of the application")
    parser.addoption("--branch", default="master", help="The branch of the current build")
    parser.addoption("--env", default="python-dev", help="The environment of the current build")
    parser.addoption("--proxy", type=validate_server_api, help="Go through proxy server. Must be of the form: http[s]://<server>")


def pytest_configure(config):
    conf.app["customer_id"] = config.getoption("customer_id")
    conf.app["app_name"] = config.getoption("app_name")
    conf.app["server"] = config.getoption("server")
    conf.app["build"] = config.getoption("build")
    conf.app["branch"] = config.getoption("branch")
    conf.app["env"] = config.getoption("env")
    conf.app["proxy"] = config.getoption("proxy")

    import pkg_resources
    print "before - " + str(pkg_resources.get_distribution("sealights-python-agent").version)
    auto_upgrade = AutoUpgrade("sealights-python-agent", conf.app["server"], conf.app["customer_id"])
    auto_upgrade.upgrade()
    print "after - " + str(pkg_resources.get_distribution("sealights-python-agent").version)

    logging.config.dictConfig(conf.LOG_CONF)
    config_logging()
    config.pluginmanager.register(SealightsPlugin())
