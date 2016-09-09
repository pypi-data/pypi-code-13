from kryptal.pluginmanager import IStorageProvider


class LocalFolder(IStorageProvider.IStorageProvider):
    def name(self):
        return "LocalFolder"
