import re
import os

from django.contrib.staticfiles.finders import get_finders
from django.utils.lru_cache import lru_cache

equal = lambda o, o2: o == o2
basename = lambda p: os.path.basename(p)

is_css = lambda name: bool(re.match(r'.*\.(css|min\.css)$', name))
is_js = lambda name: bool(re.match(r'.*\.(js|min\.js)$', name))
is_img = lambda name: bool(re.match(r'.*\.(jpg|jpeg|png|tif|gif)$', name))


@lru_cache(maxsize=1000)
def get_static_file(name):
    for finder in get_finders():
        for path, _ in finder.list('none'):
            if equal(path, name) or \
               equal(basename(path), name):
                return path
    raise FileNotFoundError('File %s does not exists' % name)
