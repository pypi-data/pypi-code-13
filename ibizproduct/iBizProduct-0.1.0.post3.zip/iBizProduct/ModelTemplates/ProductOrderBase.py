from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from iBizProduct.Contracts.ProductOrderSpec import ProductOrderSpec

class ProductOrderBase(with_metaclass(ABCMeta)):
    
    @abstractmethod
    def __init__(self, orderSpec):
        pass

    @property
    @abstractmethod
    def ProductOrderId(self):
        pass

    @property
    @abstractmethod
    def Cost(self):
        pass

    @property
    @abstractmethod
    def Setup(self):
        pass

    @property
    @abstractmethod
    def ProductOrderName(self):
        pass

    @property
    @abstractmethod
    def ProductOrderStatus(self):
        pass

    @property
    @abstractmethod
    def Notes(self):
        pass