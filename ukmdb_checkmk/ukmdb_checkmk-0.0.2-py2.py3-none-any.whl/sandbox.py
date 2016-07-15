"""
my sandbox for wato testing
"""
# pylint: disable=C0103

import argparse
import pprint
import logging
from ukmdb_checkmk import host as wato_host

CLIENT_LOG = logging.getLogger("wato_webapi")
WATO_LOG = logging.getLogger("wato_cmds")

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", required=True, type=str,
                    help="username for connect with database")
parser.add_argument("-p", "--password", required=True, type=str,
                    help="password for connect with database")
parser.add_argument("--debug-wato",
                    help="enable wato commands tracing (maybe several times)",
                    action="count",
                    default=0)

args = parser.parse_args()

if args.debug_wato:
    if args.debug_wato == 1:
        WATO_LOG.setLevel(logging.WARNING)
        WATO_LOG.warning(u"2Debugging wato with level: 'WARNING'")
    elif args.debug_wato == 2:
        WATO_LOG.setLevel(logging.INFO)
        WATO_LOG.info(u"2Debugging wato with level: 'INFO'")
    elif args.debug_wato > 2:
        WATO_LOG.setLevel(logging.DEBUG)
        WATO_LOG.debug(u"2Debugging wato with level: 'DEBUG'")
else:
    WATO_LOG.setLevel(logging.ERROR)

print("-" * 80)

CONTEXT = {'username': args.username,
           'password': args.password}

c_mk_host01 = wato_host.CheckMkHost(context=CONTEXT,
                                    folder='Tests',
                                    hostname='Hase')

print("starting .. 100 ..")
for i in range(100):
    a = c_mk_host01.attributes['ipaddress']

print("IP address after 100 get requests")
pprint.pprint(c_mk_host01.attributes['ipaddress'])


print("-" * 80)

pprint.pprint(c_mk_host01.attributes['alias'])
pprint.pprint(c_mk_host01.alias)

c_mk_host01.alias += '_dd'
c_mk_host01.commit()

print("-" * 80)

exit(0)
