import os
from importlib import import_module

from babel.messages import Catalog
from babel.messages.pofile import read_po
from django.apps import apps as app_registry
from django.core.exceptions import ImproperlyConfigured


def merge_catalogs(catalogs):
    """
    Merge the given Catalogs, ruthlessly replacing (not augmenting) content.

    :param catalogs: List of catalogs
    :type catalogs: Iterable[babel.messages.Catalog]
    :return: New catalog
    :rtype: babel.messages.Catalog
    """
    merged_catalog = None
    for catalog in catalogs:
        if catalog is None:
            continue
        if merged_catalog is None:
            merged_catalog = Catalog(
                locale=str(catalog.locale or 'en'),
                charset=catalog.charset
            )
        assert catalog.charset == merged_catalog.charset
        for msg in catalog:
            if not msg.id:
                continue
            merged_catalog.delete(msg.id)
            merged_catalog[msg.id] = msg
    return merged_catalog


def merge_catalog_files(catalog_filenames):
    catalogs = []
    for filename in catalog_filenames:
        with open(filename, 'rb') as infp:
            catalogs.append(read_po(infp))
    return merge_catalogs(catalogs)


def yes(*args, **kwargs):
    return True


def get_paths(apps=(), dirs=(), dir_children=(), all_apps=False, dirname_filter=yes):
    paths = set()
    if apps or all_apps:
        for app_config in app_registry.get_app_configs():
            if all_apps or app_config.name in apps:
                paths.add(os.path.realpath(app_config.path))

    paths.update(set(os.path.realpath(dir) for dir in dirs))

    for parent_dir in dir_children:
        parent_dir = os.path.realpath(parent_dir)
        for dir in os.listdir(parent_dir):
            if os.path.isdir(dir) and dirname_filter(dir):
                paths.add(dir)

    return paths


def add_paths_options(parser):
    parser.add_argument('--all-apps', action='store_true')
    parser.add_argument('-a', '--app', action='append', dest='apps', default=[])
    parser.add_argument('-d', '--dir', action='append', dest='dirs', default=[])
    parser.add_argument(
        '--dir-children',
        action='append',
        dest='dir_children',
        help='add immediate directory children of this directory as dirs',
        default=[]
    )


def raise_if_no_module(module):
    try:
        import_module(module)
    except ImportError:
        raise ImproperlyConfigured("`%s` is required for this functionality" % module)


class DirectoryFilter(object):
    def __init__(self, ignore_dirs=(), default_ignore_dirs=True):
        self.ignore_dirs = ignore_dirs
        self.default_ignore_dirs = default_ignore_dirs

    def matches(self, path):
        basename = os.path.basename(path)
        if basename[0] in {'.', '_'}:
            return False
        if self.default_ignore_dirs:
            if basename in {'bower_components', 'node_modules', 'tests', 'htmlcov'}:
                return False
        return (basename not in self.ignore_dirs)

    def __call__(self, path):
        return self.matches(path)

    @classmethod
    def add_options(cls, parser):
        parser.add_argument('-I', '--ignore-dir', action='append', dest='ignore_dirs', default=[])
        parser.add_argument('--no-default-ignore-dirs', dest='default_ignore_dirs', action='store_false', default=True)
