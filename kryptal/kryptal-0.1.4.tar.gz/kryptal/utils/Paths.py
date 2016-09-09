import sys, os
import jpath


def exe_path():
    if hasattr(sys, "frozen") and sys.frozen in ("windows_exe", "console_exe"):
        return jpath.path(os.path.abspath(sys.executable)).dirname()
    else:
        return os.path.dirname(sys.argv[0])


def plugin_path():
    return os.path.join(exe_path(), "plugins")


def plugin_path_filesystems():
    return os.path.join(plugin_path(), "filesystems")


def plugin_path_storageproviders():
    return os.path.join(plugin_path(), "storageproviders")
