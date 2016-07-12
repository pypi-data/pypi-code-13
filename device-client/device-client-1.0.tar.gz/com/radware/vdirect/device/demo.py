import pprint

from com.radware.vdirect.device.meta.dp8 import DP8Meta
from com.radware.vdirect.device.meta.alteon import AlteonMeta
from com.radware.vdirect.device.meta.appwall661 import AppWall661Meta
from com.radware.vdirect.device.client import get_client


pp = pprint.PrettyPrinter(indent=4)


def p(result, msg):
    print msg
    pp.pprint(result)
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'


vdirect_ip = '10.205.120.114'

registered_dp_name = '10.205.124.21'
client = get_client(vdirect_ip, registered_dp_name)

meta = DP8Meta()

msg = 'Fetch all'
p(client.read(meta.ifEntry()), msg)

msg = 'Fetch all records but only a subset of the fields'
p(client.read(meta.ifEntry(), projection=[meta.ifEntry.inOctets, meta.ifEntry.inDiscards]), msg)

msg = 'Fetch all records (that satisfies the filter) but only a subset of the fields'
p(client.read(meta.ifEntry(), projection=[meta.ifEntry.inOctets, meta.ifEntry.inDiscards, meta.ifEntry.descr],
                 filter_func=lambda x: x[meta.ifEntry.descr] == 'FortyGige-1'), msg)

msg = 'Fetch all records but only a subset of the fields'
p(client.read(meta.ifEntry(), projection=[meta.ifEntry.inOctets, meta.ifEntry.inDiscards, meta.ifEntry.index],
                 index_entries=[{'key': meta.ifEntry.index, 'value': 7}], sort_key=meta.ifEntry.inUnknownProtos), msg)

meta = AlteonMeta()
registered_alteon_name = '10.205.122.90'
client = get_client('10.205.120.114', registered_alteon_name)

msg = 'Fetch all records From alteon'
p(client.read(meta.realServerGroupCfg(), projection=[meta.realServerGroupCfg.slbGroupTableMaxSize,
                                                            meta.realServerGroupCfg.slbGroupMaxIdsSize]), msg)

meta = AppWall661Meta()
registered_appwall_name = '10.205.122.220'
client = get_client('10.205.122.138', registered_appwall_name)

msg = 'Fetch all records From appwal'
p(client.read(meta.httpsTunnelsEntry(), projection=[meta.httpsTunnelsEntry.activeConnections,
                                                            meta.httpsTunnelsEntry.enableServerIdentity]), msg)


