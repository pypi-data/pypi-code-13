from xmlrpclib import ProtocolError
from xmlrpclib import Fault as RPCFault

class Fault(Exception):
    """
    This error class exists to standardise certain xmlrpclib.Fault and
    xmlrpclib.ProtocolError instances under a single interface that conforms
    to the Adestra MessageFocus documentation.
    """
    def __init__(self, faultCode, faultString):
        super(Exception, self).__init__("%s: %s" % (faultCode, faultString))
        self.faultCode = faultCode
        self.faultString = faultString
        pass

    @staticmethod
    def parse(fn):
        def func_wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if isinstance(e, ProtocolError):
                    if e.errcode == 401:
                        raise Fault(301, "You must be authenticated to use this resource.")
                if isinstance(e, RPCFault):
                    if e.faultCode == 200:
                        # Fault code 200 is undocumented by MessageFocus but frequently
                        # used and could mean many things. Typically it has similar meaning
                        # to 204, i.e. the type or sequence of arguments does not match the
                        # method signature.
                        #
                        # The full fault string sometimes includes specifics about failed SQL
                        # queries and perl modules. This information is rarely useful and should
                        # not be visible to begin with for security reasons.
                        #
                        # Below we attempt to rewrite these errors into shorter more
                        # useful error messages
                        if "invalid input syntax for integer" in e.faultString:
                            # An example case where this might crop up is if you manage
                            # to insert a string value where an integer is expected.
                            raise Fault(204, "Argument invalid or of incorrect type, e.g. you have passed a String where an Integer is expected.")
                        elif "column" in e.faultString and "does not exist" in e.faultString:
                            # This is a SQL error where an invalid table name has somehow
                            # made its way in to the query.
                            #
                            # There are likely many ways of achieving this failure,
                            # I have put in place safeguards for some. E.g. attempting to
                            # use a non-empty dictionary instead of an integer for the
                            # core_table_id.
                            raise Fault(204, "Argument invalid or of incorrect type, e.g. you have passed a Struct where an Integer is expected.")
                        elif "Campaign has not been published" in e.faultString:
                            # This error code has been added to those published by Adestra since I first encountered it,
                            # I am leaving the special handling in in the event that it was not done properly on their end.
                            raise Fault(216, "Campaign has not been published.")
                    raise Fault(e.faultCode, e.faultString)
                raise e
        return func_wrapper