#!/usr/bin/env python
# coding: utf8

from apps.views.archive import ArchiveHandler
from apps.views.index import IndexHandler
from apps.views.page import PageHandler
from apps.views.post import PostHandler
from apps.views.tag import TagHandler
from apps.views.category import CategoryHandler

handlers = [
    (r'/(\d+)?', IndexHandler),
    (r'/archive/(\d{4})/(\d{2})', ArchiveHandler),
    (r'/category/(\w+)', CategoryHandler),
    (r'/tag/(\w+)', TagHandler),
    (r'/(\d{4})/(\d{2})/(\d{2})/(\w+)', PostHandler),
    (r'/(\w+)', PageHandler),
]
