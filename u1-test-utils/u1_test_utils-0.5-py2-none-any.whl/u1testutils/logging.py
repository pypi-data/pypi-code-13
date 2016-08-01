from __future__ import absolute_import

import logging
from unittest import TestCase


# Originally written by:
#    - Guillermo Gonzalez
#    - Facundo Batista
#    - Natalia Bidart
class LogHandlerTestCase(TestCase):
    """A mixin that adds a memento loghandler for testing logging."""

    class MementoHandler(logging.Handler):
        """A handler class which stores logging records in a list.

        From http://nessita.pastebin.com/mgc85uQT
        """
        def __init__(self, *args, **kwargs):
            """Create the instance, and add a records attribute."""
            logging.Handler.__init__(self, *args, **kwargs)
            self.records = []

        def emit(self, record):
            """Just add the record to self.records."""
            self.records.append(record)

        def check(self, level, msg, check_traceback=False):
            """Check that something is logged."""
            result = False
            for rec in self.records:
                if rec.levelname == level:
                    result = str(msg) in rec.getMessage()
                    if not result and check_traceback:
                        result = str(msg) in rec.exc_text
                    if result:
                        break

            return result

    def setUp(self):
        """Add the memento handler to the root logger."""
        super(LogHandlerTestCase, self).setUp()
        self.memento_handler = self.MementoHandler()
        self.root_logger = logging.getLogger()
        self.root_logger.addHandler(self.memento_handler)

    def tearDown(self):
        """Remove the memento handler from the root logger."""
        self.root_logger.removeHandler(self.memento_handler)
        super(LogHandlerTestCase, self).tearDown()

    def assertLogLevelContains(self, level, message, check_traceback=False):
        check = self.memento_handler.check(
            level, message, check_traceback=check_traceback)

        msg = ('Expected logging message/s could not be found:\n%s\n'
               'Current logging records are:\n%s')
        expected = '\t%s: %s' % (level, message)
        records = ['\t%s: %s' % (r.levelname, r.getMessage())
                   for r in self.memento_handler.records]
        self.assertTrue(check, msg % (expected, '\n'.join(records)))
