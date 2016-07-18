from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class EventBase(with_metaclass(ABCMeta)):
    
    @property
    @abstractmethod
    def EventId(self):
        pass

    @property
    @abstractmethod
    def ProductOrderId(self):
        pass

    @property
    @abstractmethod
    def EventRequested(self):
        pass

    @property
    @abstractmethod
    def APIRequests(self):
        pass

    @property
    @abstractmethod
    def EventCompleted(self):
        pass

    @property
    @abstractmethod
    def Type(self):
        pass

    @property
    @abstractmethod
    def IsQueued(self):
        pass