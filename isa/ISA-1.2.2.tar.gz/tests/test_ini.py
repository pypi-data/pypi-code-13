#!/usr/bin/env python
# -*- coding: utf-8 -*-

from isa.exceptions import CircularException
from isa.ini import parse_nodes
from isa.util import create_file, remove_file

try:
    from ConfigParser import NoOptionError
except ImportError:
    from configparser import NoOptionError
from unittest import TestCase

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestINI(TestCase):
    def check_subset(self, subset, fullset):
        """
        Check whether the set of all keys of subset equals the set of all keys of fullset and check whether all
        properties in subset are contained in fullset.

        :param subset: the subset to check
        :param fullset: the fullset to check
        """
        assert subset.keys() == fullset.keys(), "Subset keys should equal fullset keys: %s == %s" % (
        subset.keys(), fullset.keys())
        for key in subset:
            for subkey in subset[key]:
                assert subkey in fullset[key]
                assert subset[key][subkey] == fullset[key][subkey]

    def test_flag_enabled(self):
        """ Test the enabled flag. """
        # Only one disabled
        ini = create_file("""
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
        remove_file(ini)
        ini = create_file("""
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
        remove_file(ini)

    def test_flag_host(self):
        """ Test the host flag. """
        ini = create_file("""
            [node1]
            enabled = True
            """)
        self.assertRaises(NoOptionError, parse_nodes, ini.name)
        remove_file(ini)

    def test_flag_via_circular(self):
        """ Test the circular exception """
        ini = create_file("""
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
        remove_file(ini)

    def test_flag_via(self):
        """ Test the via flag """
        ini = create_file("""
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
        self.assertEqual(nodes['node1']['via-chain'], ['node3', 'node2'])
        self.assertEqual(nodes['node2']['via-chain'], ['node3'])
        self.assertEqual(nodes['node3']['via-chain'], [])
        remove_file(ini)
