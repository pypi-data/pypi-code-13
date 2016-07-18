from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class FAQMessageBase(with_metaclass(ABCMeta)):
    @property
    @abstractmethod
    def FAQMessageId(self):
        pass

    @property
    @abstractmethod
    def FAQId(self):
        pass

    @property
    @abstractmethod
    def Language(self):
        pass

    @property
    @abstractmethod
    def Title(self):
        pass

    @property
    @abstractmethod
    def Content(self):
        pass