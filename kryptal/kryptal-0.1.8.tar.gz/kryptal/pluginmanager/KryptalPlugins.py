from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginManager import PluginManager

from kryptal.pluginmanager.IFilesystem import IFilesystem
from kryptal.pluginmanager.IStorageProvider import IStorageProvider
from kryptal.utils import Paths


class KryptalPlugins(object):
    def __init__(self):
        self._filesystemPlugins = _FilesystemPlugins()
        self._storageProviderPlugins = _StorageProviderPlugins()
        print(Paths.plugin_paths())

    def filesystems(self):
        return self._filesystemPlugins.all()

    def storage_providers(self):
        return self._storageProviderPlugins.all()


class _PluginManagerBase(object):
    def __init__(self, directories, categories):
        locator = PluginFileLocator()
        locator.setPluginInfoExtension("kryptal-plugin")
        locator.setPluginPlaces(directories)
        self._manager = PluginManager()
        self._manager.setCategoriesFilter(categories)
        self._manager.setPluginLocator(locator)

    def all(self):
        self._manager.collectPlugins()
        return [p.plugin_object for p in self._manager.getAllPlugins()]


class _FilesystemPlugins(_PluginManagerBase):
    def __init__(self):
        super(_FilesystemPlugins, self).__init__(Paths.plugin_paths_filesystems(), {"Filesystem": IFilesystem})


class _StorageProviderPlugins(_PluginManagerBase):
    def __init__(self):
        super(_StorageProviderPlugins, self).__init__(Paths.plugin_paths_storageproviders(), {"StorageProvider": IStorageProvider})
