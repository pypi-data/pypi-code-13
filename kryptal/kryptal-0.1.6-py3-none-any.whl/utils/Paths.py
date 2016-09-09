import os
from kryptal import plugins


def plugin_path():
    return os.path.dirname(plugins.__file__)

def plugin_path_filesystems():
    return os.path.join(plugin_path(), "filesystems")

def plugin_path_storageproviders():
    return os.path.join(plugin_path(), "storageproviders")
