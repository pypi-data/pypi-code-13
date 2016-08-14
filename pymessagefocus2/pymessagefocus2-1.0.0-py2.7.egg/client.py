from xmlrpclib import ServerProxy
from transport import Transport

class Client(ServerProxy):
    def __init__(self, organisation, username, password, verbose=False):
        ServerProxy.__init__(self,
                             "https://%s.%s:%s@app.adestra.com/api/xmlrpc" % (organisation, username, password),
                             transport=Transport(use_datetime=True),
                             encoding="UTF-8",
                             allow_none=True,
                             verbose=verbose)
        pass
    pass