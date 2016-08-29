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
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed
from mezzanine.blog.feeds import PostsRSS
from mezzanine.conf import settings


class HubRss201rev2Feed(Rss201rev2Feed):
    def add_root_elements(self, handler):
        super(Rss201rev2Feed, self).add_root_elements(handler)
        hub = self.feed.get('hub')
        if hub is not None:
            for elem in hub:
                handler.addQuickElement('atom:link', '', {'rel': 'hub',
                                                          'href': elem})


class HubAtom1Feed(Atom1Feed):
    def add_root_elements(self, handler):
        super(Atom1Feed, self).add_root_elements(handler)
        hub = self.feed.get('hub')
        if hub is not None:
            for elem in hub:
                handler.addQuickElement('link', '', {'rel': 'hub',
                                                     'href': elem})


class HubPostsRSS(PostsRSS):
    feed_type = HubRss201rev2Feed
    hub = None

    def get_hub(self, obj):
        if self.hub is None:
            hub = getattr(settings, 'PUSH_HUB', None)
        else:
            hub = self.hub
        return hub

    def feed_extra_kwargs(self, obj):
        kwargs = super(PostsRSS, self).feed_extra_kwargs(obj)
        kwargs['hub'] = self.get_hub(obj)
        return kwargs


class HubPostsAtom(HubPostsRSS):
    """
    Atom feed for all blog posts.
    """

    feed_type = HubAtom1Feed

    def subtitle(self):
        return self.description()
