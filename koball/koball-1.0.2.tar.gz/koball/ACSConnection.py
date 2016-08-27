from aliyunsdkcore import client

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from six.moves import configparser
from collections import defaultdict

from ecs.region import Region
try:
    import json
except ImportError:
    import simplejson as json


class ACSConnection(object):
    def __init__(self):
        self.conn = None
    
    def get_all_regions(self, connect_args):
        cache_region = 'cn-hangzhou'
        try:
            all_regions = []
            conn = client.AcsClient(connect_args.get('acs_access_key_id'), connect_args.get('acs_secret_access_key'), cache_region)
            request = DescribeRegionsRequest.DescribeRegionsRequest()
            request.set_accept_format('json')
            regions = json.loads(conn.do_action(request))['Regions']['Region']
            for region in regions:
                all_regions.append(Region(region.get('RegionId', None), region.get('LocalName', None)))
            return all_regions
        except:
            raise

ACSConnection()
