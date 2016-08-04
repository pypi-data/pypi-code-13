# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from video_brain.graph_parser.visualizator import Visualizator
import pickle

class TestVisualizator(TestCase):

    def test_visualize(self):

        visualizator = Visualizator()
        visualizator.visualize('/home/leo/Desktop/graph_deep_residual/water_plant_sky_snow_cloud_rock_beach_sand_vegetation/database/')

if __name__ == '__main__':
    unittest.main()