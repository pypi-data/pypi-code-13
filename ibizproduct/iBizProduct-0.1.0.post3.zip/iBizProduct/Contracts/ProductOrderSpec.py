from abc import abstractmethod
from iBizProduct.Contracts.iBizSpec import iBizSpec

class ProductOrderSpec(iBizSpec):
    @property
    @abstractmethod
    def ProductOrderId(self):
        pass
    @ProductOrderId.setter
    @abstractmethod
    def setProductOrderId(ProductOrderId):
        pass

    @property
    @abstractmethod
    def ProductOrderName(self):
        pass
    @ProductOrderName.setter
    @abstractmethod
    def setProductOrderName(self, ProductOrderName):
        pass

    @property
    @abstractmethod
    def Cost(self):
        pass
    @Cost.setter
    @abstractmethod
    def setCost(self, Cost):
        pass

    @property
    @abstractmethod
    def Setup(self):
        pass
    @Setup.setter
    @abstractmethod
    def setSetup(self, Setup):
        pass

    @property
    @abstractmethod
    def ProductOrderStatus(self):
        pass
    @ProductOrderStatus.setter
    @abstractmethod
    def setProductOrderStatus(self, ProductOrderStatus):
        pass

    @property
    @abstractmethod
    def Notes(self):
        pass
    @Notes.setter
    @abstractmethod
    def setNotes(self, Notes):
        pass