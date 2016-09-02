"""
   Copyright 2016 Kem

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import unicode_literals

import requests
from django.core.urlresolvers import resolve
from mezzanine.conf import settings
from mezzanine.utils.tests import TestCase
from mezzanine_pubsubhubbub_pub import PROTOCOL_TYPE_HTTP, PROTOCOL_TYPE_HTTPS, PROTOCOL_TYPE_BOTH, UA
from mezzanine_pubsubhubbub_pub.models import HubBlogPost

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def mocked_requests_post(*args, **kwargs):
    return "mockResponse"


class HubBlogPostTest(TestCase):
    def setUp(self):
        self.tmp_settings = settings

    def tearDown(self):
        settings = self.tmp_settings

    @patch.object(requests, "post", side_effect=mocked_requests_post)
    def test_no_notify(self, mock_post):
        blog_post = HubBlogPost()
        blog_post.user_id = 1
        blog_post.status = 1
        settings.PUSH_URL_PROTOCOL = PROTOCOL_TYPE_HTTP
        blog_post.save()
        self.assertFalse(mock_post.called)

    @patch.object(requests, "post", side_effect=mocked_requests_post)
    def test_notify_http(self, mock_post):
        blog_post = HubBlogPost()
        blog_post.user_id = 1
        blog_post.status = 2
        settings.PUSH_URL_PROTOCOL = PROTOCOL_TYPE_HTTP
        blog_post.save()

        call_args_list = mock_post.call_args_list
        call = call_args_list[0]
        expected = self.__create_extpected('http://example.com/blog/feeds/rss/')
        self.assertEqual(expected, call)

        call = call_args_list[1]
        expected = self.__create_extpected('http://example.com/blog/feeds/atom/')
        self.assertEqual(expected, call)

    @patch.object(requests, "post", side_effect=mocked_requests_post)
    def test_notify_https(self, mock_post):
        blog_post = HubBlogPost()
        blog_post.user_id = 1
        blog_post.status = 2
        settings.PUSH_URL_PROTOCOL = PROTOCOL_TYPE_HTTPS
        blog_post.save()

        call_args_list = mock_post.call_args_list
        call = call_args_list[0]
        expected = self.__create_extpected('https://example.com/blog/feeds/rss/')
        self.assertEqual(expected, call)

        call = call_args_list[1]
        expected = self.__create_extpected('https://example.com/blog/feeds/atom/')
        self.assertEqual(expected, call)

    @patch.object(requests, "post", side_effect=mocked_requests_post)
    def test_notify_both(self, mock_post):
        blog_post = HubBlogPost()
        blog_post.user_id = 1
        blog_post.status = 2
        settings.PUSH_URL_PROTOCOL = PROTOCOL_TYPE_BOTH
        blog_post.save()

        call_args_list = mock_post.call_args_list
        call = call_args_list[0]
        expected = self.__create_extpected('http://example.com/blog/feeds/rss/')
        self.assertEqual(expected, call)

        call = call_args_list[1]
        expected = self.__create_extpected('http://example.com/blog/feeds/atom/')
        self.assertEqual(expected, call)

        call = call_args_list[2]
        expected = self.__create_extpected('https://example.com/blog/feeds/rss/')
        self.assertEqual(expected, call)

        call = call_args_list[3]
        expected = self.__create_extpected('https://example.com/blog/feeds/atom/')
        self.assertEqual(expected, call)

    @staticmethod
    def __create_extpected(feed_url):
        return (('https://pubsubhubbub.appspot.com/',), {"data": {'hub.url': feed_url,
                                                                  'hub.mode': u'publish'}, "headers": {
            'User-Agent': UA}},)


class BlogPostFeedTest(TestCase):
    def setUp(self):
        super(BlogPostFeedTest, self).setUp()
        self.tmp_settings = settings

    def tearDown(self):
        settings = self.tmp_settings

    @patch.object(requests, "post", side_effect=mocked_requests_post)
    def test_feed_atom(self, mock_post):
        resolver_match = resolve('/blog/feeds/atom/')
        blog_post_feed = resolver_match.func
        # Create an instance of a GET request.
        from mezzanine.core.request import _thread_local
        request = self._request_factory.get('/blog/feeds/atom/')
        request.site_id = settings.SITE_ID
        _thread_local.request = request
        response = blog_post_feed(request, format=resolver_match.kwargs['format'])
        import xml.etree.ElementTree as ET
        root = ET.fromstringlist(response._container)
        elem = root.find("{http://www.w3.org/2005/Atom}link")

        self.assertEqual('hub', elem.attrib['rel'])
        self.assertEqual('https://pubsubhubbub.appspot.com/', elem.attrib['href'])

    def test_feed_rss(self):
        resolver_match = resolve('/blog/feeds/rss/')
        blog_post_feed = resolver_match.func
        # Create an instance of a GET request.
        from mezzanine.core.request import _thread_local
        request = self._request_factory.get('/blog/feeds/rss/')
        request.site_id = settings.SITE_ID
        _thread_local.request = request
        response = blog_post_feed(request, format=resolver_match.kwargs['format'])

        import xml.etree.ElementTree as ET
        root = ET.fromstringlist(response._container)
        elems = root.findall(".//{http://www.w3.org/2005/Atom}link")

        for elem in elems:
            if 'hub' == elem.attrib.get('rel', None):
                self.assertEqual('https://pubsubhubbub.appspot.com/', elem.attrib['href'])
            else:
                print("-----------------")
                print("elem.attrib=" + str(elem.attrib))
                print("-----------------")
