from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class EventMessageBase(with_metaclass(ABCMeta)):
    
    @property
    @abstractmethod
    def FAQId(self):
        pass

    @property
    @abstractmethod
    def DefaultLanguage(self):
        pass