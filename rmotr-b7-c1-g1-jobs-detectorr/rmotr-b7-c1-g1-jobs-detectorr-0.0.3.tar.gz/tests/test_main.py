# -*- coding: utf-8 -*-
import re
import os
import unittest

import responses
from click.testing import CliRunner

from jobs_detector import settings
from jobs_detector.main import jobs_detector

import warnings
warnings.filterwarnings("ignore")

class HackerNewsTestCase(unittest.TestCase):

    def setUp(self):
        self.post_id = '11814828'
        fixture_path = os.path.join(settings.BASE_DIR, 'tests',
                                    'fixtures', '{}.html'.format(self.post_id))
        with open(fixture_path) as f:
            content = f.read()
        responses.add(responses.GET,
                      re.compile(re.escape(settings.BASE_URL.format(self.post_id))),
                      body=content, status=200,
                      content_type='text/html')

    @responses.activate
    def test_hacker_news_default_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news', '-i', self.post_id]
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Remote: 174 (19%)',
            'Postgres: 81 (9%)',
            'Python: 143 (16%)',
            'Javascript: 118 (13%)',
            'React: 133 (15%)',
            'Pandas: 5 (0%)',
        ]
        for msg in expected:
            #import ipdb; ipdb.set_trace()
            
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_custom_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django']
        )
        expected = [
            'Total job posts: 883',
            'Keywords:',
            'Python: 143 (16%)', #was 186, 16%
            'Django: 36 (4%)', #was 44, 4%
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)
        # self.assertTrue(expected[0] in result.output)
    @responses.activate
    def test_hacker_news_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Remote: 174 (19%)',
            'Postgres: 81 (9%)',
            'Python: 143 (16%)',
            'Javascript: 118 (13%)',
            'React: 133 (15%)',
            'Pandas: 5 (0%)',

            'Combinations:',
            'Python-Remote: 25 (2%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (3%)',
        ]
        for msg in expected:
            # import ipdb; ipdb.set_trace()
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_keywords_and_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django',
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Python: 143 (16%)',
            'Django: 36 (4%)',

            'Combinations:',
            'Python-Remote: 25 (2%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (3%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)