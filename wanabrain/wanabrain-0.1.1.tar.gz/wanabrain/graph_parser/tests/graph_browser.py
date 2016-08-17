# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from wanabrain.graph_parser.graph_browser import GraphBrowser
import time

class TestGraphBrowser(TestCase):

    def test_fit(self):

        graph_browser = GraphBrowser()
        # graph_browser.fit('/home/leo/Desktop/graph/', 'deep_residual')

        graph_browser.fit('/home/leo/Desktop/graph_deep_residual/', 'deep_residual')
        # graph_browser.fit('/home/leo/Desktop/graph_alexnet/', 'alexnet')

if __name__ == '__main__':
    unittest.main()