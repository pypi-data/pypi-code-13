from __future__ import print_function

import os
import errno
import shutil
import unittest
import tempfile
import datetime

import pyconfreader

class TestCase(unittest.TestCase):
    def assertConf(self, result, d):
        self.assertEqual(result._asdict(), d)


class SimpleTestCase(TestCase):

    def test_simple(self):
        self.assertConf(pyconfreader.loads('i=3'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('i=3\n'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('\ni=3\n'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('i="3"\nj=i*2'),
                        {'i': '3', 'j': '33'})

    def test_other_globals(self):
        def f(arg):
            return arg*arg

        self.assertConf(pyconfreader.loads('x=fn(3)', globals={'fn':f}),
                        {'x': 9})

    def test_underscore_ignored(self):
        self.assertConf(pyconfreader.loads('_i=10\ni=_i+5'),
                        {'i': 15})

    def test_locals(self):
        locals = {'i': 10}
        self.assertConf(pyconfreader.loads('i *= 3', locals=locals),
                        {'i': 30})

        # and make sure the locals were updated
        self.assertEqual(locals, {'i': 30})


class TestSimpleLoader(TestCase):
    def setUp(self):
        # create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # remove the directory after the test
        shutil.rmtree(self.test_dir)

    def write_file(self, filename, contents):
        filename = os.path.join(self.test_dir, filename)

        # create the directory, in case we're writing to a subdirectory
        dirname = os.path.dirname(filename)
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirname):
                pass
            else:
                raise

        with open(filename, 'w') as fl:
            fl.write(contents)

    def with_files(self, file_map, default_file, d, fl_validator=None):
        for filename, contents in file_map.items():
            self.write_file(os.path.join(self.test_dir, filename), contents)

        loader = pyconfreader.SimpleFileLoader(self.test_dir, fl_validator=fl_validator)
        self.assertConf(loader(default_file), d)

    def test_loader(self):
        self.with_files({'foo.cfg': '''
x = 3
''',
                         },
                        'foo.cfg',
                        {'x': 3})

    def test_loader_include(self):
        self.with_files({'foo.cfg': '''
x = 3
include('bar.cfg')
''',
                         'bar.cfg': '''
j=x*3
''',
                         },
                        'foo.cfg',
                        {'x': 3, 'j': 9})

    def test_loader_include_import(self):
        self.with_files({'foo.cfg': '''
_day = 19
x=3
# make sure we can use the imported module in the included file
import datetime as _datetime
include('bar.cfg')
''',
                         'bar.cfg': '''
j=_datetime.date(2016, 8, _day)
''',
                         },
                        'foo.cfg',
                        {'x': 3, 'j': datetime.date(2016, 8, 19)})

    def test_validator(self):
        def validator(fl, filename):
            if os.path.basename(filename) == 'bar.cfg':
                raise ValueError('cannot load {}: {}'.format(fl, filename))

        self.assertRaises(ValueError, self.with_files,
                          {'foo.cfg': '''
include('bar.cfg')
''',
                           'bar.cfg': '''
x=0
''',
                           },
                          'foo.cfg',
                          {'x': 3, 'j': datetime.date(2016, 8, 19)},
                          fl_validator=validator)


unittest.main()
