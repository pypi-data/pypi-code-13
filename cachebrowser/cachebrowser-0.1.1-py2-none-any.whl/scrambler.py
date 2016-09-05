from random import random, shuffle, choice
from time import time, sleep
from threading import Thread, RLock

from six.moves.urllib.parse import urlparse
from mitmproxy.models import HTTPResponse
from netlib.http import Headers

from cachebrowser.pipes.base import FlowPipe
from cachebrowser.util import get_flow_size, pretty_bytes


ORGS = [
    ('GOOGLE', ['google']),
    ('AKAMAI', ['akamai', 'umass']),
    ('AMAZON', ['at-', 'amazo']),
    # ('CLOUDFRONT', []),
    ('FASTLY', ['fastly']),
    ('CLOUDFLARE', ['cloudflare']),
    ('EDGECAST', ['edgecast']),
    ('HIGHWINDS', ['highwind']),
    ('INCAPSULA', ['incapsula']),
    ('MAXCDN', ['netdna']),
    ('CDNET', ['cdnet']),
    ('TWITTER', ['twitter']),
    ('INAP', ['inap-']),
    ('LINODE', ['linode']),
    ('DIGITALOCEAN', ['digitalocean']),
    ('YAHOO', ['yahoo']),
    ('FACEBOOK', ['facebook', 'ord1', 'tfbnet']),

    ('OTHER', [])
]

ORG_NAMES = [x[0] for x in ORGS]

DOWNSTREAM_STD = 100000



def should_i(prob):
    return random() < prob


class Scrambler(FlowPipe):
    PROB_AD_BLOCK = 1.0
    PROB_AD_DECOY = 1.0
    PROB_DECOY = 0.2

    OVERHEAD = 0.1
    BLOCK_ADS = True

    def __init__(self, *args, **kwargs):
        super(Scrambler, self).__init__(*args, **kwargs)

        self.adblocker = AdBlocker()
        self.netstats = NetStatKeeper()
        self.decoymaker = DecoyMaker(self.netstats)

        self.block_count = 0
        self.notblock_count = 0

        self.upstream_overhead = 0
        self.upstream_traffic = 0       # Non-Overhead traffic
        self.downstream_overhead = 0
        self.downstream_traffic = 0
        self.decoysent = 0
        self.decoyreceived = 0

        self.user_requests = 0
        self.blocked_requests = 0

    def start(self):
        # super(Scrambler, self).start()
        self.adblocker.load_blacklist()
        self.decoymaker.load_decoys()

    def reset(self):
        self.block_count = 0
        self.notblock_count = 0
        self.netstats.reset()

        self.upstream_overhead = 0
        self.upstream_traffic = 0       # Non-Overhead traffic
        self.downstream_overhead = 0
        self.downstream_traffic = 0
        self.decoysent = 0
        self.decoyreceived = 0
        self.decoymaker.inflight = 0

        self.user_requests = 0
        self.blocked_requests = 0
        self.decoymaker.current_decoy = None

    def get_stats(self):
        return {
            'blocked': 0,
            'upstream_overhead': self.upstream_overhead,
            'upstream_normal': self.upstream_traffic,
            'downstream_overhead': self.downstream_overhead,
            'downstream_normal': self.downstream_traffic,
            'decoys': self.decoyreceived,
            'decoys_sent': self.decoysent,
            'max_overhead': self.OVERHEAD,
            'user_requests': self.user_requests,
            'blocked_requests': self.blocked_requests,
            'adblock_enabled': self.BLOCK_ADS
        }

    def serverconnect(self, server_conn):
        pass

    def print_stats(self):
        print(self.decoymaker.inflight)
        print("Sent: {}  Received: {}  Overhead: {}  Traffic: {}   Overhead: {}  Traffic: {} ".format(self.decoysent, self.decoyreceived,
                                                                         pretty_bytes(self.downstream_overhead), pretty_bytes(self.downstream_traffic),
                                                                          pretty_bytes(self.upstream_overhead), pretty_bytes(self.upstream_traffic)))

    def request(self, flow):
        is_decoy = hasattr(flow, 'is_decoy') and flow.is_decoy

        if is_decoy:
            self.netstats.update_real_upstream(flow)
            self.upstream_overhead += get_flow_size(flow)[0]

            self.decoysent += 1
        else:
            self.netstats.update_requested_upstream(flow)
            self.user_requests += 1

            if self.BLOCK_ADS and self.adblocker.should_block(flow):
                self.blocked_requests += 1
                self.dummy_response(flow)
                # self._send_decoy_request(skip_netname=_whois(flow))
                self._send_decoy_request()
            else:
                self.netstats.update_real_upstream(flow)
                self.upstream_traffic += get_flow_size(flow)[0]

                wanted = sum(self.netstats.requested_downstream_traffic.values())
                actual = sum(self.netstats.real_downstream_traffic.values())
                if actual + self.decoymaker.inflight < wanted + wanted * self.OVERHEAD:
                    self._send_decoy_request()

                # self._send_decoy_request()

        # self.print_stats()
        # print("")
        self.log('>> {}  {} '.format(self.notblock_count, self.block_count))

    def response(self, flow):
        is_decoy = hasattr(flow, 'is_decoy') and flow.is_decoy

        if is_decoy:
            self.netstats.update_real_downstream(flow)
            self.decoymaker.record_decoy_received(flow)
            self.decoyreceived += 1

            self.downstream_overhead += get_flow_size(flow)[1]
        else:
            self.netstats.update_real_downstream(flow)
            self.netstats.update_requested_downstream(flow)
            self.downstream_traffic += get_flow_size(flow)[1]

    def _send_decoy_request(self):
        if self.decoymaker.current_decoy is None:
            decoy = self.decoymaker.select_decoy()
            self.log("Selecting {} as decoy".format(decoy))
            # print("Selecting {} as decoy".format(decoy))

        decoyurl = self.decoymaker.get_decoy_url()
        if decoyurl is not None:
            new_flow = self.create_request_from_url('GET', decoyurl)

            # Don't update stats on dummy request
            new_flow.outgoing_request = True
            new_flow.is_decoy = True
            self.send_request(new_flow, run_hooks=True)

            self.decoymaker.record_decoy_sent(new_flow, decoyurl)

    # def _send_decoy_request(self, skip_netname=None):
    #     decoyurl = self.decoymaker.get_decoy_url(skip_netname)
    #     self.log("Sending DECOY to {}".format(decoyurl))
    #     if decoyurl is not None:
    #         new_flow = self.create_request_from_url('GET', decoyurl)
    #
    #         # Don't update stats on dummy request
    #         new_flow.outgoing_request = True
    #         new_flow.is_decoy = True
    #         self.send_request(new_flow, run_hooks=True)
    #
    #         self.decoymaker.record_decoy_sent(decoyurl)

    def handle_ads(self, flow):
        domain = urlparse(flow.request.url).netloc

        if self.adblocker.should_block(flow) and should_i(self.PROB_AD_BLOCK):
            self.dummy_response(flow)

            if should_i(self.PROB_AD_DECOY):
                decoy_url = self.decoymaker.get_decoy_url(flow)
                if decoy_url is not None:
                    self.log("@@@@@@@@@@@@@@  Sending Decoy Request {}".format(decoy_url))
                    new_flow = self.create_request_from_url('GET', decoy_url)

                    # Don't update stats on dummy request
                    new_flow.outgoing_request = True
                    new_flow.is_dummy = True
                    self.send_request(new_flow, run_hooks=True)

            return True

        return False

    def dummy_response(self, flow):
        resp = HTTPResponse(
            "HTTP/1.1", 444, "Blocked",
            Headers(Content_Type="text/html"),
            "You got blocked by CDNReaper")
        flow.reply(resp)

    def error(self, flow):
        pass


class NetStatKeeper(object):
    UPSTREAM_STD = 200
    DOWNSTREAM_STD = DOWNSTREAM_STD

    S = 10

    def __init__(self):
        from collections import deque

        self.requested_upstream = {}
        self.requested_downstream = {}
        self.requested_upstream_traffic = {}
        self.requested_downstream_traffic = {}

        self.real_upstream = {}
        self.real_downstream = {}
        self.real_upstream_traffic = {}
        self.real_downstream_traffic = {}

        self.lock = RLock()
        # self.outgoing_lock = RLock()

        for org in ORG_NAMES:
            self.requested_upstream[org] = deque()
            self.requested_downstream[org] = deque()
            self.real_downstream[org] = deque()
            self.real_upstream[org] = deque()
            self.real_downstream_traffic[org] = 0
            self.real_upstream_traffic[org] = 0
            self.requested_downstream_traffic[org] = 0
            self.requested_upstream_traffic[org] = 0

        def refresher():
            def refresh(ds):
                for k in ds:
                    while len(ds[k]):
                        if ds[k][0][0] < threshold:
                            ds[k].popleft()
                        else:
                            break

            while True:
                sleep(1)
                now = time()
                threshold = now - self.S

                with self.lock:
                    refresh(self.requested_downstream)
                    refresh(self.requested_upstream)
                    refresh(self.real_downstream)
                    refresh(self.real_upstream)

                    for netname in ORG_NAMES:
                        self.requested_upstream_traffic[netname] = 0
                        for item in self.requested_upstream[netname]:
                            self.requested_upstream_traffic[netname] += item[1]

                        self.requested_downstream_traffic[netname] = 0
                        for item in self.requested_downstream[netname]:
                            self.requested_downstream_traffic[netname] += item[1]

                        self.real_upstream_traffic[netname] = 0
                        for item in self.real_upstream[netname]:
                            self.real_upstream_traffic[netname] += item[1]

                        self.real_downstream_traffic[netname] = 0
                        for item in self.real_downstream[netname]:
                            self.real_downstream_traffic[netname] += item[1]

        refresh_thread = Thread(target=refresher)
        refresh_thread.daemon = True
        refresh_thread.start()

    def update_requested_downstream(self, flow):
        ip = _get_flow_ip(flow)
        if ip is None:
            return

        _, resp = get_flow_size(flow)

        netname = _whois(ip)
        with self.lock:
            self.requested_downstream_traffic[netname] += resp
            self.requested_downstream[netname].append((time(), resp))

    def update_requested_upstream(self, flow):
        ip = _get_flow_ip(flow)
        if ip is None:
            return

        req, _ = get_flow_size(flow)

        netname = _whois(ip)
        with self.lock:
            self.requested_upstream_traffic[netname] += req
            self.requested_upstream[netname].append((time(), req))

    def update_real_downstream(self, flow):
        ip = _get_flow_ip(flow)
        if ip is None:
            return

        _, resp = get_flow_size(flow)

        netname = _whois(ip)
        with self.lock:
            self.real_downstream_traffic[netname] += resp
            self.real_downstream[netname].append((time(), resp))

    def update_real_upstream(self, flow):
        ip = _get_flow_ip(flow)
        if ip is None:
            return

        req, _ = get_flow_size(flow)

        netname = _whois(ip)
        with self.lock:
            self.real_upstream_traffic[netname] += req
            self.real_upstream[netname].append((time(), req))

    def reset(self):
        with self.lock:
            for key in self.requested_downstream:
                self.requested_downstream[key].clear()
                self.requested_upstream[key].clear()
                self.real_downstream[key].clear()
                self.real_upstream[key].clear()


class DecoyMaker(object):
    def __init__(self, netstats):
        self.netstats = netstats
        # self.decoy_urls = {}
        # self.decoy_sizes = {}
        self.decoys = {}
        self.current_decoy = None
        self.current_decoy_index = 0

        self.inflight = 0

        self.sizes = {}

    def select_decoy(self):
        decoy = choice(self.decoys.keys())
        self.current_decoy = self.decoys[decoy]
        self.current_decoy_index = 0
        return decoy

    def get_decoy_url(self):
        if self.current_decoy is None:
            return None
        if self.current_decoy_index >= len(self.current_decoy):
            return None

        decoy_url = self.current_decoy[self.current_decoy_index]['url']
        size = self.current_decoy[self.current_decoy_index]['response_size']

        self.sizes[decoy_url] = size

        self.current_decoy_index += 1
        if self.current_decoy_index >= len(self.current_decoy):
            self.current_decoy = None

        return decoy_url

    def record_decoy_sent(self, flow, url):
        size = self.sizes[url]
        flow.estimated_size = size
        self.inflight += size

    def record_decoy_received(self, flow):
        self.inflight -= flow.estimated_size

    def load_decoys(self):
        import yaml
        # json loads strings as unicode, causes problems with saving flows
        with open('data/decoys.json') as f:
            decoy_urls = yaml.safe_load(f.read())
            self.decoys = decoy_urls


class AdBlocker(object):
    def __init__(self):
        self.single_dom = set()
        self.multi_dom = set()
        self.adset = set()

        self.blacklist = []

    def should_block(self, flow):
        from fnmatch import fnmatch

        domain = urlparse(flow.request.url).netloc

        parts = domain.split('.')
        dom = parts.pop()
        while parts:
            dom = '{}.{}'.format(parts.pop(), dom)
            if dom in self.adset:
                return True

        url = flow.request.url.replace('https://', '').replace('http://', '')
        for pattern in self.blacklist:
            if fnmatch(url, pattern):
                return True

        return False

    def load_blacklist(self):
        with open('data/ad-domains') as f:
            for ad in f:
                ad = ad.strip()
                if not ad: continue
                if ad.count('.') == 1:
                    self.single_dom.add(ad)
                else:
                    self.multi_dom.add(ad)
                self.adset.add(ad)

        with open('data/blacklist') as f:
            for dom in f:
                dom = dom.strip()
                if dom:
                    self.blacklist.append(dom)


def _get_flow_ip(flow):
    if flow.server_conn and flow.server_conn.peer_address:
        return flow.server_conn.peer_address.host

    domain = urlparse(flow.request.url).netloc
    ips, domains = _dig(domain)
    if len(ips):
        return ips[0]
    return None


_whois_cache = {}


def _whois(ip):
    from ipwhois import IPWhois

    if type(ip) is not str:
        ip = _get_flow_ip(ip)

    if ip not in _whois_cache:
        whois = IPWhois(ip)
        try:
            name = whois.lookup_rdap()['network']['name']
            if not name:
                name = whois.lookup()['nets'][0]['name']
        except:
            print("WHOIS ERROR")
            name = 'OTHER'

        _whois_cache[ip] = _clean_netname(name, ip)
    return _whois_cache[ip]


def _clean_netname(name, ip):
    name = name.lower()

    for org in ORGS:
        if any([x in name for x in org[1]]):
            return org[0]

    return 'OTHER'


def _parse_dig(raw_dig):
    import re

    if len(raw_dig.strip()) == 0:
        return [], []

    lines = raw_dig.strip().split('\n')

    ip = []
    domains = []
    for line in lines:
        line = line.strip()
        if re.match('^\d+[.]\d+[.]\d+[.]\d+$', line):
            ip.append(line)
        else:
            domains.append(line)

    return ip, domains


def _dig(site, raw=False):
    from subprocess import Popen, PIPE
    process = Popen(["dig", "+short", site], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    if raw:
        return output

    return _parse_dig(output)
