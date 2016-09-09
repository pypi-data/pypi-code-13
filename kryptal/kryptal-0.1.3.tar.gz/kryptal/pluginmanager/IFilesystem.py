from abc import ABCMeta, abstractmethod
from yapsy.IPlugin import IPlugin


class IFilesystem(IPlugin, metaclass=ABCMeta):
    @abstractmethod
    def name(self):
        pass
