from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class iBizSpec(with_metaclass(ABCMeta)):
    @property
    def Spec(self):
        pass

    @Spec.getter
    @abstractmethod
    def getSpec(self):
        pass