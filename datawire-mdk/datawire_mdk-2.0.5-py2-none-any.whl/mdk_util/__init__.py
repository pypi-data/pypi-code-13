# Quark 1.0.406 run at 2016-08-31 17:18:17.189918
from quark_runtime import *

import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime.promise
import quark
import datawire_mdk_md


class WaitForPromise(_QObject):
    """
    Utility to blockingly wait for a Promise to get a value.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def _finished(self, value, done):
        (done).acquire();
        (done).wakeup();
        (done).release();
        return True

    @staticmethod
    def wait(p, timeout, description):
        snapshot = (p).value();
        if ((snapshot).hasValue()):
            return (snapshot).getValue()

        done = _Condition();
        waiter = WaitForPromise();
        (p).andThen(quark._BoundMethod(waiter, u"_finished", _List([done])));
        msTimeout = long(round((timeout) * (1000.0)));
        (done).acquire();
        (done).waitWakeup(msTimeout);
        (done).release();
        snapshot = (p).value()
        if (not ((snapshot).hasValue())):
            raise Exception((u"Timeout waiting for ") + (description));

        return (snapshot).getValue()

    def _getClass(self):
        return u"mdk_util.WaitForPromise"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
WaitForPromise.mdk_util_WaitForPromise_ref = None

def toNativePromise(p):
    if (not (False)):
        raise Exception(u"This method only works on Javascript.");

    return


def extend(list, value, size):
    while ((len(list)) < (size)):
        (list).append(value);



def versionMatch(requested, actual):
    if ((requested) == (None)):
        return True

    reqparts = (requested).split(u".");
    actparts = (actual).split(u".");
    extend(reqparts, u"0", 3);
    extend(actparts, u"0", 3);
    if (((reqparts)[0]) != ((actparts)[0])):
        return False

    if (((actparts)[1]) > ((reqparts)[1])):
        return True

    if (((actparts)[1]) < ((reqparts)[1])):
        return False

    return ((actparts)[2]) >= ((reqparts)[2])
