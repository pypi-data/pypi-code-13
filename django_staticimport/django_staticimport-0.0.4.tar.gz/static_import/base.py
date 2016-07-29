import re
import os
import copy

from django.contrib.staticfiles.finders import get_finders
from django.core.exceptions import ImproperlyConfigured
from django.utils.lru_cache import lru_cache

from static_import.settings import get_config


equal = lambda o, o2: o == o2
basename = lambda p: os.path.basename(p)

REMOTE = 'remote'
LOCAL = 'local'
is_remote = lambda o: equal(o, REMOTE)
is_local = lambda o: equal(o, LOCAL)

is_css = lambda name: bool(re.match(r'.*\.(css|min\.css)$', name))
is_js = lambda name: bool(re.match(r'.*\.(js|min\.js)$', name))
is_img = lambda name: bool(re.match(r'.*\.(jpg|jpeg|png|tif|gif)$', name))


def safe_extra_attrs(_attrs):
    attrs = copy.deepcopy(_attrs)
    style = attrs.get('style', None)
    if style is not None:
        style = style.replace('"', "'")
        attrs['style'] = style

    return attrs


def _try(dict, key, error_msg):
    try:
        dict[key]
    except KeyError:
        raise ImproperlyConfigured(error_msg)


def get_libs():
    libs = get_config()
    for lib in libs:
        _try(lib, 'name', 'Library name have not been set.')
        _try(lib, 'url', 'Library url have not been set.')
        yield lib


@lru_cache(maxsize=None)
def get_static_file(name):
    for finder in get_finders():
        for path, _ in finder.list('none'):
            if equal(path, name) or \
               equal(basename(path), name):
                return path, LOCAL

    for lib in get_libs():
        remote_lib_name = lib['name']
        remote_lib_location = lib['url']

        if equal(remote_lib_name, name):
            return remote_lib_location, REMOTE

    raise FileNotFoundError('File %s does not exists' % name)
