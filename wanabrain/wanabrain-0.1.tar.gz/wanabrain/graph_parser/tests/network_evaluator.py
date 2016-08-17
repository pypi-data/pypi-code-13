# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from wanabrain.graph_parser.network_evaluator import NetworkEvaluator

class TestGraphBrowser(TestCase):

    def test_fit(self):

        labels = ['water', 'plant', 'sky', 'snow', 'cloud', 'rock', 'beach', 'sand', 'vegetation']

        network_evaluator = NetworkEvaluator()
        network_evaluator.eval_network('/home/leo/Desktop/graph_deep_residual/water_plant_sky_snow_cloud_rock_beach_sand_vegetation/', labels)

if __name__ == '__main__':
    unittest.main()