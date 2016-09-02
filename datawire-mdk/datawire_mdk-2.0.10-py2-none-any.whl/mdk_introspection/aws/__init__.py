# Quark 1.0.406 run at 2016-09-02 10:11:28.675365
from quark_runtime import *

import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_introspection
import mdk_runtime
import datawire_mdk_md


class Ec2Host(_QObject):
    def _init(self):
        self.scope = None
        self.env = None

    def __init__(self, env, scope):
        self._init()
        (self).scope = (scope).upper()
        (self).env = env

    @staticmethod
    def metadataHost(env):
        return ((env).var(u"DATAWIRE_METADATA_HOST_OVERRIDE")).orElseGet(u"169.254.169.254")

    def get(self):
        if ((self.scope) == (u"INTERNAL")):
            return _url_get(((u"http://") + (Ec2Host.metadataHost(self.env))) + (u"/latest/meta-data/local-hostname"))

        if ((self.scope) == (u"PUBLIC")):
            return _url_get(((u"http://") + (Ec2Host.metadataHost(self.env))) + (u"/latest/meta-data/public-hostname"))

        return _cast(None, lambda: unicode)

    def _getClass(self):
        return u"mdk_introspection.aws.Ec2Host"

    def _getField(self, name):
        if ((name) == (u"scope")):
            return (self).scope

        if ((name) == (u"env")):
            return (self).env

        return None

    def _setField(self, name, value):
        if ((name) == (u"scope")):
            (self).scope = _cast(value, lambda: unicode)

        if ((name) == (u"env")):
            (self).env = _cast(value, lambda: mdk_runtime.EnvironmentVariables)


Ec2Host.mdk_introspection_aws_Ec2Host_ref = None
