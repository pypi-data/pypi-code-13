from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class ProductAuthentication(with_metaclass(ABCMeta)):
    @property
    @abstractmethod
    def Action(self):
        pass

    @Action.setter
    @abstractmethod
    def setAction(self, Action):
        pass

    @property
    @abstractmethod
    def SessionID(self):
        pass
    @SessionID.setter
    @abstractmethod
    def setSetSessionID(self, SessionID):
        pass

    @property
    @abstractmethod
    def Language(self):
        pass
    @Language.setter
    @abstractmethod
    def setLanguage(self, Language):
        pass

    @property
    @abstractmethod
    def MyAccountID(self):
        pass
    @MyAccountID.setter
    @abstractmethod
    def setMyAccountID(self, MyAccountID):
        pass

    @property
    @abstractmethod
    def AccountID(self):
        pass
    @AccountID.setter
    @abstractmethod
    def setAccountID(self, AccountID):
        pass

    @property
    @abstractmethod
    def OfferID(self):
        pass
    @OfferID.setter
    @abstractmethod
    def setOfferID(self, OfferID):
        pass

    @property
    @abstractmethod
    def ProductOrderID(self):
        pass
    @ProductOrderID.setter
    @abstractmethod
    def setProductOrderID(self, ProductOrderID):
        pass