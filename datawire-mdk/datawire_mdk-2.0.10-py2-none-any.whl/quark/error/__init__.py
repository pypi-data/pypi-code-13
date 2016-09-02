# Quark 1.0.406 run at 2016-09-02 10:11:28.675365
from quark_runtime import *

import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import datawire_mdk_md


class Error(_QObject):
    def _init(self):
        self.message = None

    def __init__(self, message):
        self._init()
        (self).message = message

    def getMessage(self):
        return self.message

    def toString(self):
        return ((u"Error(") + ((self).message)) + (u")")

    def _getClass(self):
        return u"quark.error.Error"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


Error.quark_error_Error_ref = None
