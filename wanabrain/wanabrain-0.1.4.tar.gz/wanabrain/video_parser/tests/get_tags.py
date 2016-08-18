# -*- coding: utf-8 -*-
from unittest import TestCase
from wanabrain.video_parser import VideoParser

class TestBrowsing(TestCase):

    def test_graph_browsing(self):


        video_parser = VideoParser(['../../../../../rushs/AF-AFR-01-003_500k.f4v'])

        tags = video_parser.get_tags_naive()
        print(tags)

