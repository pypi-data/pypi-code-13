from abc import abstractmethod, abstractproperty
from typing import Any, Dict

from plenum.persistence.wallet_storage import WalletStorage as PWalletStorage


class WalletStorage(PWalletStorage):
    @abstractmethod
    def addAttribute(self, name: str, val: Any, origin: str, dest: str=None,
                     encKey: str=None, encType: str=None, hashed: bool=False):
        pass

    @abstractmethod
    def getAttribute(self, name: str, dest: str=None):
        pass

    @abstractproperty
    def attributes(self):
        pass

    @abstractmethod
    def addCredDef(self, name: str, version: str, dest: str, type: str, ip: str,
                     port: int, keys: Dict):
        pass

    @abstractmethod
    def getCredDef(self, name: str, version: str, dest: str = None):
        pass

    @abstractmethod
    def addCredential(self, name: str, data: Dict):
        pass

    @abstractmethod
    def getCredential(self, name: str):
        pass
