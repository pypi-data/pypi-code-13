from xmlrpclib import SafeTransport
from fault import Fault

class Transport(SafeTransport):
    def __init__(self, **kwargs):
        SafeTransport.__init__(self, **kwargs)
        pass

    @Fault.parse
    def single_request(self, *args, **kwargs):
        return SafeTransport.single_request(self, *args, **kwargs)