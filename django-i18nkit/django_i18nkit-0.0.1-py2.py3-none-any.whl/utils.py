import os
from importlib import import_module

from django.apps import apps as app_registry
from django.core.exceptions import ImproperlyConfigured

from babel.messages import Catalog
from babel.messages.pofile import read_po


def merge_catalogs(catalogs):
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


def raise_if_no_module(module):
    try:
        import_module(module)
    except ImportError:
        raise ImproperlyConfigured("`%s` is required for this functionality" % module)
