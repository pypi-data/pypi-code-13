import logging

import blpapi

_bbglogger = logging.getLogger("BBG")


BLP_DATE = blpapi.Name("date")
BLP_ERROR_INFO = blpapi.Name("errorInfo")
BLP_EVENT_TIME = blpapi.Name("EVENT_TIME")
BLP_FIELD_DATA = blpapi.Name("fieldData")
BLP_FIELD_EXCEPTIONS = blpapi.Name("fieldExceptions")
BLP_FIELD_ID = blpapi.Name("fieldId")
BLP_SECURITY = blpapi.Name("security")
BLP_SECURITY_DATA = blpapi.Name("securityData")
BLP_CURVE_MEMBERS = blpapi.Name("CURVE_MEMBERS")
BLP_CRNCY = blpapi.Name("CRNCY")
BLP_COUNTRY = blpapi.Name("COUNTRY")

