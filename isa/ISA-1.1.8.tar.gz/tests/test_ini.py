#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap

from isa.exceptions import CircularException
from isa.ini import parse_nodes

try:
    from ConfigParser import NoOptionError
except ImportError:
    from configparser import NoOptionError
from unittest import TestCase
import tempfile
import os

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestINI(TestCase):
    @staticmethod
    def create_ini_file(content):
        """
        Create an INI file.

        :param content: the contents to put into the INI file
        :return: the file handle to the INI file
        """
        ini = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        ini.write(textwrap.dedent(content))
        ini.seek(0)
        return ini

    @staticmethod
    def remove_ini_file(ini):
        """
        Remove an INI file.

        :param ini: the file handle to the INI file
        """
        return os.unlink(ini.name)

    def check_subset(self, subset, fullset):
        """
        Check whether the set of all keys of subset equals the set of all keys of fullset and check whether all
        properties in subset are contained in fullset.

        :param subset: the subset to check
        :param fullset: the fullset to check
        """
        assert subset.keys() == fullset.keys(), "Subset keys should equal fullset keys: %s == %s" % (subset.keys(), fullset.keys())
        for key in subset:
            for subkey in subset[key]:
                assert subkey in fullset[key]
                assert subset[key][subkey] == fullset[key][subkey]

    def test_flag_enabled(self):
        """ Test the enabled flag. """
        # Only one disabled
        ini = TestINI.create_ini_file("""
            [node1]
            host = 127.0.0.1
            enabled = False

            [node2]
            host = 127.0.0.2
            """)
        nodes = parse_nodes(ini.name)
        self.check_subset({
            'node1': {
                'host': '127.0.0.1',
                'enabled': False
            },
            'node2': {
                'host': '127.0.0.2',
                'enabled': True
            }
        }, nodes)

        # Now all disabled
        TestINI.remove_ini_file(ini)
        ini = TestINI.create_ini_file("""
            [node1]
            host = 127.0.0.1
            enabled = False

            [node2]
            host = 127.0.0.2
            enabled = False
            """)
        nodes = parse_nodes(ini.name)
        self.check_subset({
            'node1': {
                'host': '127.0.0.1',
                'enabled': False
            },
            'node2': {
                'host': '127.0.0.2',
                'enabled': False
            }
        }, nodes)
        TestINI.remove_ini_file(ini)

    def test_flag_host(self):
        """ Test the host flag. """
        ini = TestINI.create_ini_file("""
            [node1]
            enabled = True
            """)
        self.assertRaises(NoOptionError, parse_nodes, ini.name)
        TestINI.remove_ini_file(ini)

    def test_flag_via_circular(self):
        """ Test the circular exception """
        ini = TestINI.create_ini_file("""
            [node1]
            host = 127.0.0.1
            enabled = True
            via = node2

            [node2]
            host = 127.0.0.2
            enabled = True
            via = node3

            [node3]
            host = 127.0.0.3
            enabled = False
            via = node1
            """)
        self.assertRaises(CircularException, parse_nodes, ini.name)
        TestINI.remove_ini_file(ini)

    def test_flag_via(self):
        """ Test the via flag """
        ini = TestINI.create_ini_file("""
            [node1]
            host = 127.0.0.1
            via = node2

            [node2]
            host = 127.0.0.2
            via = node3

            [node3]
            host = 127.0.0.3
            """)
        nodes = parse_nodes(ini.name)
        print(nodes)
        self.assertEqual(nodes['node1']['via-chain'], ['node3', 'node2'])
        self.assertEqual(nodes['node2']['via-chain'], ['node3'])
        self.assertEqual(nodes['node3']['via-chain'], [])
        TestINI.remove_ini_file(ini)