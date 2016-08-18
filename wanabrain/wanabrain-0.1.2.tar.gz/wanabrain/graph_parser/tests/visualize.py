# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from wanabrain.graph_parser.visualizator import Visualizator
import pickle

class TestVisualizator(TestCase):

    def test_visualize(self):

        visualizator = Visualizator()
        # visualizator.visualize_tags('/home/leo/Desktop/graph_deep_residual/person_animal_nature_man_work/database/')
        visualizator.visualize_landscape('/home/leo/Desktop/database/')

if __name__ == '__main__':
    unittest.main()