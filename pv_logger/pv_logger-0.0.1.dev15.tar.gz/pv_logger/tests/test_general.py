import unittest as unittest
import os
try:
    from unittest import mock
except ImportError:
    import mock

from pv_logger import logger as pvlogger

class GeneralTest(unittest.TestCase):
    def test_inverter_type_unknown(self):
        pvlogger.Config.config['inverter_type'] = 'unknown'

        try:
            pvlogger.main_loop()
        except Exception as e:
            if 'unknown' in str(e):
                pass
            else:
                raise
