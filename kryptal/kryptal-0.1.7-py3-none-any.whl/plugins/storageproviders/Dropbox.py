from kryptal.pluginmanager import IStorageProvider


class Dropbox(IStorageProvider.IStorageProvider):
    def name(self):
        return "Dropbox"
