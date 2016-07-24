import os
import tempfile
import unittest
from .util import patch

import hark_builder.context


class TestBuilderContext(unittest.TestCase):

    @patch('hark.dal.DAL._connect')
    @patch('os.mkdir')
    def test_initialize(self, patchMkdir, patchConnect):
        td = tempfile.mkdtemp()
        hark_builder.context.BuilderContext(td)

        expectPath = os.path.join(td, 'builder')
        patchMkdir.assert_any_call(expectPath)
