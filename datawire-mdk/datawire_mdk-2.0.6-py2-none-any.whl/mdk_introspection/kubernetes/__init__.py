# Quark 1.0.406 run at 2016-08-31 18:17:52.891343
from quark_runtime import *

import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_introspection
import datawire_mdk_md


class KubernetesHost(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def get(self):
        return _cast(None, lambda: unicode)

    def _getClass(self):
        return u"mdk_introspection.kubernetes.KubernetesHost"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
KubernetesHost.mdk_introspection_kubernetes_KubernetesHost_ref = None
class KubernetesPort(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def get(self):
        return _cast(None, lambda: int)

    def _getClass(self):
        return u"mdk_introspection.kubernetes.KubernetesPort"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
KubernetesPort.mdk_introspection_kubernetes_KubernetesPort_ref = None
