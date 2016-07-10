from com.radware.vdirect.dp.dp8 import DP8Meta
from com.radware.vdirect.dp.dp_client import DPClient

import pprint

pp = pprint.PrettyPrinter(indent=4)

def p(result, msg):
    print msg
    pp.pprint((result))
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

vdirect_ip = '10.205.120.114'
registered_dp_name = '10.205.124.21'
client = DPClient(vdirect_ip, registered_dp_name)

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
              index_entries=[{'key': 'index', 'value': 7}]), msg)




