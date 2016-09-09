import os
from kryptal import plugins
from appdirs import AppDirs


_appdirs = AppDirs("Kryptal")

def plugin_paths():
    return [
        os.path.dirname(plugins.__file__), # Plugins packaged with the Kryptal distribution
        os.path.join(_appdirs.user_data_dir, "plugins"), # Plugins installed for this user only (on Linux: /home/user/.local/share/Kryptal/plugins)
        os.path.join(_appdirs.site_data_dir, "plugins") # Plugins installed for all users (on Linux: /usr/local/share/Kryptal/plugins)
    ]

def plugin_paths_filesystems():
    return [os.path.join(path, "filesystems") for path in plugin_paths()]

def plugin_paths_storageproviders():
    return [os.path.join(path, "storageproviders") for path in plugin_paths()]
