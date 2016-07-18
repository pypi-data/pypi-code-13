from abc import abstractmethod
from iBizProduct.Contracts.iBizSpec import iBizSpec

class EventStatus(iBizSpec):  
    @property
    def EventStatus(self):
        pass

    @EventStatus.getter
    @abstractmethod
    def getEventStatus(self):
        pass