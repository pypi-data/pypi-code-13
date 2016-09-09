from kryptal.pluginmanager import IFilesystem


class CryFS(IFilesystem.IFilesystem):
    def name(self):
        return "CryFS"
