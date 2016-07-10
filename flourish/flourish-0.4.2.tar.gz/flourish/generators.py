from datetime import datetime
from math import ceil
import os
import warnings

from pyatom import AtomFeed


class BaseGenerator(object):
    order_by = None
    paginate_by = None

    @classmethod
    def as_generator(cls):
        def generator(flourish, url, global_context=None):
            self = cls(flourish, url, global_context)
            return self.generate()

        return generator

    def __init__(self, flourish, url, global_context):
        self.flourish = flourish
        self.url = url
        self.global_context = global_context
        self.current_url = None

    def get_paginator(self, objects, filter):
        if self.paginate_by:
            # FIXME orphans?
            _num_pages = int(ceil(len(objects) / float(self.paginate_by)))
            _start = 0
            _pages = []
            _paginator = {
                'num_pages': _num_pages,
                'pages': [],
            }
            for _i in range(1, _num_pages + 1):
                _end = _start + self.paginate_by
                _pages.append(objects[_start:_end])
                _start = _start + self.paginate_by
                _path = self.url.resolve(**filter)
                if _path.endswith('/'):
                    if _i > 1:
                        _path_page = 'page-%s' % (_i)
                        _path = '%s%s' % (_path, _path_page)
                else:
                    # FIXME test this
                    warnings.warn('paginated URL "%s" must end in "/" in '
                                  'order to paginate correctly' % _path)

                _paginator['pages'].append({
                    'url': _path,
                    'number': _i,
                })
            return (_pages, _paginator)
        return (objects, None)

    def generate(self):
        for _filter in self.flourish.all_valid_filters_for_url(self.url.name):
            _objects = self.get_objects(_filter)
            _page_objects, _paginator = self.get_paginator(_objects, _filter)
            if _paginator:
                for _count, _page in enumerate(_page_objects):
                    _path = _paginator['pages'][_count]['url']
                    self.current_url = _path
                    _context = self.get_context_data(_page)
                    if self.global_context is not None:
                        _context['global'] = self.global_context(self)
                    _paginator['current_page'] = _count + 1
                    _context['pagination'] = _paginator
                    _template = self.get_template(_page)
                    _render = self.render_template(_template, _context)
                    _filename = self.get_output_filename(_path)
                    self.output_to_file(_filename, _render)
            else:
                _path = self.url.resolve(**_filter)
                self.current_url = _path
                _context = self.get_context_data(_objects)
                if self.global_context is not None:
                    _context['global'] = self.global_context(self)
                _template = self.get_template(_objects)
                _render = self.render_template(_template, _context)
                _filename = self.get_output_filename(_path)
                self.output_to_file(_filename, _render)

    def get_template(self, objects):
        return self.flourish.jinja.get_template(
            self.get_template_name(objects)
        )

    def get_objects(self, filter):
        _filtered = self.flourish.sources.filter(**filter)
        if self.order_by:
            _filtered = _filtered.order_by(self.order_by)
        return _filtered

    def render_template(self, template, context_data):
        return template.render(context_data).encode('UTF-8')

    def output_to_file(self, filename, render):
        _directory = os.path.dirname(filename)
        if not os.path.isdir(_directory):
            os.makedirs(_directory)
        with open(filename, 'w') as _output:
            _output.write(render)

    def get_template_name(self, objects):
        return self.template_name

    def get_output_filename(self, path):
        _destination = '%s%s' % (self.flourish.output_dir, path)
        if _destination.endswith('/'):
            _destination = _destination + 'index.html'
        if not _destination.endswith(('.html', '.atom')):
            _destination = _destination + '.html'
        return _destination

    def get_context_data(self, objects):
        _context = {}
        _context['objects'] = objects
        _context['site'] = self.flourish.site_config
        _context['current_url'] = self.current_url
        return _context


class PageGenerator(BaseGenerator):
    def get_context_data(self, objects):
        _context = super(PageGenerator, self).get_context_data(objects)
        _context['page'] = objects[0]
        _context.update(objects[0]._config)
        return _context

    def get_template_name(self, objects):
        if 'template' in objects[0]:
            return objects[0]['template']
        if 'type' in objects[0]:
            return '%s.html' % objects[0]['type']
        return 'page.html'


class IndexGenerator(BaseGenerator):
    template_name = 'index.html'

    def get_context_data(self, objects):
        _context = super(IndexGenerator, self).get_context_data(objects)
        _context['pages'] = objects
        return _context


class AtomGenerator(BaseGenerator):
    order_by = ('-published')

    def get_objects(self, filter):
        """
        Only consider objects that have the key "published" with a
        datetime value that is in the past.
        """
        _now = datetime.now()
        _only_published = self.flourish.sources.filter(published__lt=_now)
        _filtered = _only_published.filter(**filter)
        _ordered = _filtered.order_by(self.order_by)
        return _ordered

    def generate(self):
        for _filter in self.flourish.all_valid_filters_for_url(self.url.name):
            _objects = self.get_objects(_filter)
            _path = self.url.resolve(**_filter)
            _filename = self.get_output_filename(_path)

            _feed_global = {
                'author': self.flourish.site_config['author'],
                'title': self.flourish.site_config['title'],
                'url': self.flourish.site_config['base_url'],
                'feed_url': '%s%s' % (
                    self.flourish.site_config['base_url'],
                    _path,
                ),
            }
            _feed = AtomFeed(**_feed_global)

            for _object in _objects:
                entry = {
                    'title': _object.title,
                    'content': _object.body,
                    'content_type': 'html',
                    'url': _object.absolute_url,
                    'published': _object.published,
                    'updated': _object.published,
                    'author': self.flourish.site_config['author'],
                }
                try:
                    entry['author'] = _object.author
                except:
                    pass
                try:
                    entry['updated'] = _object.updated
                except:
                    pass
                _feed.add(**entry)

            self.output_to_file(_filename, _feed.to_string())
