import sys

from ufs_tools.short_decorator.ignore_exception import ignore_exc_with_result

from ufs_tools.libtool import include_all

from ufs_tools.app_tools import get_executable_folder, get_executable


# noinspection PyMethodMayBeStatic
class AppBase(object):
    def get_root_folder(self):
        return get_executable_folder()

    @ignore_exc_with_result
    def add_default_module_path(self, module_path="server_base_packages"):
        include_all(get_executable(), module_path)
