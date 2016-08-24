# -*- coding: utf-8 -*-

from unittest import TestCase
from future.builtins import bytes
from io import BytesIO
from s3fs import S3FileSystem
from ccjob import CommonCrawl

import logging

logger = logging.getLogger(__name__)

class CommonCrawlTest(TestCase):

    def setUp(self):
        self.s3 = S3FileSystem(anon=True, use_ssl=False)
        self.key = '/'.join([
            'common-crawl',
            'crawl-data',
            'CC-MAIN-2016-07',
            'segments',
            '1454702039825.90',
            'warc',
            'CC-MAIN-20160205195359-00348-ip-10-236-182-209.ec2.internal.warc.gz',
        ])
        self.s3_url = 's3://aws-publicdatasets/{key}'.format(key=self.key)

    def test_key_exists(self):
        self.assertTrue(self.s3.exists(self.s3_url))

    def test_etag(self):
        etag = self.s3.info(self.s3_url).get('ETag').strip('"')
        self.assertEqual(etag, '73e5149d26a4087534674dd7177a7371')

    def test_mapper(self):
        common_crawl = CommonCrawl()
        common_crawl.mapper_init()
        common_crawl.stderr = BytesIO()
        for (key, value), _ in common_crawl.mapper(None, self.key):
            self.assertTrue(value.isdigit())
