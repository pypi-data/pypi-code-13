from abc import abstractmethod
from iBizProduct.Contracts.iBizSpec import iBizSpec

class CaseSpec(iBizSpec):
    @property
    @abstractmethod
    def AutoClose(self):
        pass

    @AutoClose.setter
    @abstractmethod
    def setAutoClose(self, AutoClose):
        pass

    @property
    @abstractmethod
    def Description(self):
        pass

    @Description.setter
    @abstractmethod
    def setDescription(Description):
        pass

    @property
    @abstractmethod
    def Detail(self):
        pass

    @Detail.setter
    @abstractmethod
    def setDetail(self, Detail):
        pass

    @property
    @abstractmethod
    def InternalNotes(self):
        pass

    @InternalNotes.setter
    @abstractmethod
    def setInternalNotes(self, InternalNotes):
        pass

    @property
    @abstractmethod
    def IsResolved(self):
        pass

    @IsResolved.setter
    @abstractmethod
    def setIsResolved(self, IsResolved):
        pass

    @property
    @abstractmethod
    def Priority(self):
        pass

    @Priority.setter
    @abstractmethod
    def setPriority(self, Priority):
        pass

    @property
    @abstractmethod
    def ReturnHours(self):
        pass

    @ReturnHours.setter
    @abstractmethod
    def setReturnHours(self, ReturnHours):
        pass

    @property
    @abstractmethod
    def Status(self):
        pass

    @Status.setter
    @abstractmethod
    def setStatus(self, Status):
        pass

    @property
    @abstractmethod
    def Type(self):
        pass

    @Type.setter
    @abstractmethod
    def setType(self, type):
        pass