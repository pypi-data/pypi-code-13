from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class iBizAPIClientInterface(with_metaclass(ABCMeta)):
    @abstractmethod
    def ProductOrderAdd(self, productOrderSpec, productOrderId = None):
        pass
    
    @abstractmethod
    def ProductOrderEdit(self, productOrderId, productOrderSpec):
        pass

    @abstractmethod
    def ProductOrderView(self, productOrderId, infoToReturn = None):
        pass

    @abstractmethod
    def ProductOrderBillOrderAddOneTime(self, cycleBeginDate, cycleEndDate, oneTimeCost, productOrderId, detailAddon = None, descriptionAddon = None, dueNow = None):
        pass

    @abstractmethod
    def ProductOpenCaseWithOwner(self, productOrderId, caseSpec):
        pass

    @abstractmethod
    def ProductOfferPrice(self, productOrderId, accountHos, accountId = None):
        pass

    @abstractmethod
    def UpdateEvent(self, eventId, status, message):
        pass

    @abstractmethod
    def AuthenticateUser(self, productOrderAuthentication):
        pass

    @abstractmethod
    def IsValidBackendRequest(self, externalKey):
        pass

    @abstractmethod
    def ExternalKeyExists(self):
        pass

    @abstractmethod
    def VerifyExternalKey(self):
        pass