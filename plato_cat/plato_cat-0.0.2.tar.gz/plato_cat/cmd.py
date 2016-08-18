from gevent import monkey
monkey.patch_all()

import sys
import gevent
from gevent.pool import Pool

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

    monkey.patch_all()

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

    def run_case(case):
        try:
            case.run(API, gevent.sleep)
        except Exception as ex:
            exceptions.append(ex)

    pool = Pool(2)
    pool.map(run_case, cases)
    pool.join()

    if exceptions:
        pool = Pool(2)
        pool.map(lambda alert: alert.call(exceptions), alerts)
        pool.join()
