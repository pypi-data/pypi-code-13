# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import shutil
import tempfile
import warnings

import numpy

import tables
from tables.exceptions import FlavorWarning
from tables.tests import common
from tables.tests.common import allequal
from tables.tests.common import unittest
from tables.tests.common import PyTablesTestCase as TestCase


# Check read Tables from pytables version 0.8
class BackCompatTablesTestCase(TestCase):
    def test01_readTable(self):
        """Checking backward compatibility of old formats of tables."""

        if common.verbose:
            print('\n', '-=' * 30)
            print("Running %s.test01_readTable..." % self.__class__.__name__)

        # Create an instance of an HDF5 Table
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            h5file = tables.open_file(self._testFilename(self.h5fname), "r")

        try:
            table = h5file.get_node("/tuple0")

            # Read the 100 records
            result = [rec['var2'] for rec in table]
            if common.verbose:
                print("Nrows in", table._v_pathname, ":", table.nrows)
                print("Last record in table ==>", rec)
                print("Total selected records in table ==> ", len(result))

            self.assertEqual(len(result), 100)
        finally:
            h5file.close()


@unittest.skipIf(not common.lzo_avail, 'lzo not available')
class Table2_1LZO(BackCompatTablesTestCase):
    # pytables 0.8.x versions and after
    h5fname = "Table2_1_lzo_nrv2e_shuffle.h5"


@unittest.skipIf(not common.lzo_avail, 'lzo not available')
class Tables_LZO1(BackCompatTablesTestCase):
    h5fname = "Tables_lzo1.h5"  # files compressed with LZO1


@unittest.skipIf(not common.lzo_avail, 'lzo not available')
class Tables_LZO1_shuffle(BackCompatTablesTestCase):
    # files compressed with LZO1 and shuffle
    h5fname = "Tables_lzo1_shuffle.h5"


@unittest.skipIf(not common.lzo_avail, 'lzo not available')
class Tables_LZO2(BackCompatTablesTestCase):
    h5fname = "Tables_lzo2.h5"  # files compressed with LZO2


@unittest.skipIf(not common.lzo_avail, 'lzo not available')
class Tables_LZO2_shuffle(BackCompatTablesTestCase):
    # files compressed with LZO2 and shuffle
    h5fname = "Tables_lzo2_shuffle.h5"


# Check read attributes from PyTables >= 1.0 properly
class BackCompatAttrsTestCase(common.TestFileMixin, TestCase):
    FILENAME = "zerodim-attrs-%s.h5"

    def setUp(self):
        self.h5fname = TestCase._testFilename(self.FILENAME % self.format)
        super(BackCompatAttrsTestCase, self).setUp()

    def test01_readAttr(self):
        """Checking backward compatibility of old formats for attributes."""

        if common.verbose:
            print('\n', '-=' * 30)
            print("Running %s.test01_readAttr..." % self.__class__.__name__)

        # Read old formats
        a = self.h5file.get_node("/a")
        scalar = numpy.array(1, dtype="int32")
        vector = numpy.array([1], dtype="int32")
        if self.format == "1.3":
            self.assertTrue(allequal(a.attrs.arrdim1, vector))
            self.assertTrue(allequal(a.attrs.arrscalar, scalar))
            self.assertEqual(a.attrs.pythonscalar, 1)
        elif self.format == "1.4":
            self.assertTrue(allequal(a.attrs.arrdim1, vector))
            self.assertTrue(allequal(a.attrs.arrscalar, scalar))
            self.assertTrue(allequal(a.attrs.pythonscalar, scalar))


class Attrs_1_3(BackCompatAttrsTestCase):
    format = "1.3"    # pytables 1.0.x versions and earlier


class Attrs_1_4(BackCompatAttrsTestCase):
    format = "1.4"    # pytables 1.1.x versions and later


class VLArrayTestCase(common.TestFileMixin, TestCase):
    h5fname = TestCase._testFilename("flavored_vlarrays-format1.6.h5")

    def test01_backCompat(self):
        """Checking backward compatibility with old flavors of VLArray."""

        # Check that we can read the contents without problems (nor warnings!)
        vlarray1 = self.h5file.root.vlarray1
        self.assertEqual(vlarray1.flavor, "numeric")
        vlarray2 = self.h5file.root.vlarray2
        self.assertEqual(vlarray2.flavor, "python")
        self.assertEqual(vlarray2[1], [b'5', b'6', b'77'])


# Make sure that 1.x files with TimeXX types continue to be readable
# and that its byteorder is correctly retrieved.
class TimeTestCase(common.TestFileMixin, TestCase):
    # Open a PYTABLES_FORMAT_VERSION=1.x file
    h5fname = TestCase._testFilename("time-table-vlarray-1_x.h5")

    def test00_table(self):
        """Checking backward compatibility with old TimeXX types (tables)."""

        # Check that we can read the contents without problems (nor warnings!)
        table = self.h5file.root.table
        self.assertEqual(table.byteorder, "little")

    def test01_vlarray(self):
        """Checking backward compatibility with old TimeXX types (vlarrays)."""

        # Check that we can read the contents without problems (nor warnings!)
        vlarray4 = self.h5file.root.vlarray4
        self.assertEqual(vlarray4.byteorder, "little")
        vlarray8 = self.h5file.root.vlarray4
        self.assertEqual(vlarray8.byteorder, "little")


class OldFlavorsTestCase01(TestCase):
    close = False

    # numeric
    def test01_open(self):
        """Checking opening of (X)Array (old 'numeric' flavor)"""

        # Open the HDF5 with old numeric flavor
        h5fname = self._testFilename("oldflavor_numeric.h5")
        with tables.open_file(h5fname) as h5file:

            # Assert other properties in array
            self.assertEqual(h5file.root.array1.flavor, 'numeric')
            self.assertEqual(h5file.root.array2.flavor, 'python')
            self.assertEqual(h5file.root.carray1.flavor, 'numeric')
            self.assertEqual(h5file.root.carray2.flavor, 'python')
            self.assertEqual(h5file.root.vlarray1.flavor, 'numeric')
            self.assertEqual(h5file.root.vlarray2.flavor, 'python')

    def test02_copy(self):
        """Checking (X)Array.copy() method ('numetic' flavor)"""

        srcfile = self._testFilename("oldflavor_numeric.h5")
        tmpfile = tempfile.mktemp(".h5")
        shutil.copy(srcfile, tmpfile)
        try:
            # Open the HDF5 with old numeric flavor
            with tables.open_file(tmpfile, "r+") as h5file:
                # Copy to another location
                self.assertWarns(FlavorWarning,
                                 h5file.root.array1.copy, '/', 'array1copy')
                h5file.root.array2.copy('/', 'array2copy')
                h5file.root.carray1.copy('/', 'carray1copy')
                h5file.root.carray2.copy('/', 'carray2copy')
                h5file.root.vlarray1.copy('/', 'vlarray1copy')
                h5file.root.vlarray2.copy('/', 'vlarray2copy')

                if self.close:
                    h5file.close()
                    h5file = tables.open_file(tmpfile)
                else:
                    h5file.flush()

                # Assert other properties in array
                self.assertEqual(h5file.root.array1copy.flavor, 'numeric')
                self.assertEqual(h5file.root.array2copy.flavor, 'python')
                self.assertEqual(h5file.root.carray1copy.flavor, 'numeric')
                self.assertEqual(h5file.root.carray2copy.flavor, 'python')
                self.assertEqual(h5file.root.vlarray1copy.flavor, 'numeric')
                self.assertEqual(h5file.root.vlarray2copy.flavor, 'python')
        finally:
            os.remove(tmpfile)


class OldFlavorsTestCase02(TestCase):
    close = True


def suite():
    theSuite = unittest.TestSuite()
    niter = 1

    for n in range(niter):
        theSuite.addTest(unittest.makeSuite(VLArrayTestCase))
        theSuite.addTest(unittest.makeSuite(TimeTestCase))
        theSuite.addTest(unittest.makeSuite(OldFlavorsTestCase01))
        theSuite.addTest(unittest.makeSuite(OldFlavorsTestCase02))
        theSuite.addTest(unittest.makeSuite(Table2_1LZO))
        theSuite.addTest(unittest.makeSuite(Tables_LZO1))
        theSuite.addTest(unittest.makeSuite(Tables_LZO1_shuffle))
        theSuite.addTest(unittest.makeSuite(Tables_LZO2))
        theSuite.addTest(unittest.makeSuite(Tables_LZO2_shuffle))

    return theSuite


if __name__ == '__main__':
    import sys
    common.parse_argv(sys.argv)
    common.print_versions()
    unittest.main(defaultTest='suite')
