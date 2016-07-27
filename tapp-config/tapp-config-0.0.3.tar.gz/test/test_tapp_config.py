import logging
import os
import unittest
from redis import StrictRedis
from tapp_config import setup_redis, get_config, setup_logging


class TestRedis(unittest.TestCase):
    def test_setup_redis(self):
        red = setup_redis()
        assert isinstance(red, StrictRedis)
        red.set("testing", "1.2.3")
        test = red.get("testing").decode("utf-8")
        assert test == "1.2.3"


class TestGetConfig(unittest.TestCase):
    def setUp(self):
        if "TEST_CONFIG_FILE" in os.environ:
            del os.environ["TEST_CONFIG_FILE"]

    def tearDown(self):
        self.setUp()

    def test_get_default_config(self):
        cfg = get_config("test")
        assert cfg.get('db', 'SA_ENGINE_URI') == 'sqlite:////tmp/test.db'
        assert cfg.get('log', 'LOGFILE') == '/tmp/test.log'

    def test_get_environment_config(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env_cfg.ini')
        os.environ["TEST_CONFIG_FILE"] = path
        cfg = get_config("test")
        assert cfg.get('db', 'SA_ENGINE_URI') == 'sqlite:////tmp/env_test.db'
        assert cfg.get('log', 'LOGFILE') == '/tmp/env_test.log'


class TestSetupLogger(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("/tmp/*test.log")
        except OSError:
            pass
        try:
            os.remove("server.log")
        except OSError:
            pass

    def tearDown(self):
        logger = setup_logging()
        for handler in logger.handlers:
            logger.removeHandler(handler)
        for handler in logger.parent.handlers:
            logger.parent.removeHandler(handler)
        self.setUp()

    def test_setup_default_logger(self):
        logger = setup_logging()
        assert isinstance(logger, logging.getLoggerClass())
        message = 'testing 1.2.3.'
        logger.exception(message)
        assert os.path.isfile('server.log')

    def test_setup_logger(self):
        cfg = get_config("test")
        assert cfg.get('log', 'LOGFILE') == '/tmp/test.log'
        logger = setup_logging(cfg)
        assert isinstance(logger, logging.getLoggerClass())
        message = 'testing 1.2.3.'
        logger.exception(message)
        assert os.path.isfile('/tmp/test.log')



