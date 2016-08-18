import sys
from sdk.actions import api

from cases.instance import InstanceCase
from cases.key_pair import KeyPairCase
from cases.eip import EIPCase
from cases.image import ImageCase
from cases.instance_type import InstanceTypeCase
from cases.job import JobCase
from cases.monitor import MonitorCase
from cases.network import NetworkCase
from cases.operation import OperationCase
from cases.quota import QuotaCase
from cases.snapshot import SnapshotCase
from cases.volume import VolumeCase

from alerts.onealert import OneAlert
from alerts.console import ConsoleAlert


def run():
    if len(sys.argv) != 4:
        print """execute this with
%s ENDPOINT ACCESS_KEY ACCESS_SECRET""" % sys.argv[0]
        return

    API = api.setup(access_key=sys.argv[2],
                    access_secret=sys.argv[3],
                    endpoint=sys.argv[1],
                    is_debug=True)

    cases = [
        InstanceCase(),
        KeyPairCase(),
        EIPCase(),
        ImageCase(),
        InstanceTypeCase(),
        JobCase(),
        MonitorCase(),
        NetworkCase(),
        OperationCase(),
        QuotaCase(),
        SnapshotCase(),
        VolumeCase(),
    ]

    alerts = [
        # OneAlert(),
        ConsoleAlert()
    ]

    exceptions = []

    for case in cases:
        try:
            case.run(API)
        except Exception as ex:
            exceptions.append(ex)

    if exceptions:
        for alert in alerts:
            alert.call(exceptions)
