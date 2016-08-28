from aliyunsdkcore import client
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from koball.ecs.connection import ECSConnection
from koball.ecs.region import Region
try:
    import json
except ImportError:
    import simplejson as json


    
    def connect_to_region(self, region, **connect_args):
        try:
            return ECSConnection(acs_access_key=connect_args.get('acs_access_key'),
            	acs_secret_access_key=connect_args.get('acs_secret_access_key'),
            	region=region,
            	security_token=connect_args.get('security_token=', None))
        except:
            raise

    def regions(self, connect_args):
        cache_region = 'cn-hangzhou'
        try:
            all_regions = []
            conn = client.AcsClient(connect_args.get('acs_access_key_id'), connect_args.get('acs_secret_access_key'), cache_region)
            request = DescribeRegionsRequest.DescribeRegionsRequest()
            request.set_accept_format('json')
            regions = json.loads(conn.do_action(request))['Regions']['Region']
            for region in regions:
                all_regions.append(Region(region_id=region.get('RegionId', None), region_name=region.get('LocalName', None)))
            return all_regions
        except:
            raise
