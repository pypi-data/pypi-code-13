from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class FAQBase(with_metaclass(ABCMeta)):
    
    @property
    @abstractmethod
    def EventMessageId(self):
        pass

    @property
    @abstractmethod
    def EventId(self):
        pass

    @property
    @abstractmethod
    def Status(self):
        pass

    @property
    @abstractmethod
    def Message(self):
        pass

    @property
    @abstractmethod
    def Time(self):
        pass