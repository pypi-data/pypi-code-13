from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import post_resource


class NetworkCase():

    def run(self, API, sleep):
        result = API.conn.call('CreateNetwork', {
            'name': 'network-creation-case',
        })

        network_id = result['networkId']
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        networks = get_resource(API, 'DescribeNetworks', {
            'status': ['active'],
            'networkIds': [network_id]
        }, 'networkSet')

        for n in networks:
            if n['status'] != 'active':
                raise Exception('network (%s) creation job finished, but status is not [active], but [%s]' % (n['networkId'], n['status']))

        subnet_id = API.conn.call('CreateSubnet', {
            'networkId': network_id,
            'cidr': '192.168.200.0/24',
        })['subnetId']

        subnets = get_resource(API, 'DescribeSubnets', {
            'networkIds': [network_id],
            'status': ['active']
        }, 'subnetSet')

        if len(subnets) != 1:
            raise Exception('create subnet failed.')


class CleanNetworks():

    def run(self, API, sleep):
        networks = get_resource(API, 'DescribeNetworks', {
            'status': ['active']
        }, 'networkSet')

        network_ids = [n['networkId'] for n in networks if n['externalGatewayIp']]

        # unset external gateway
        post_resource(API, 'UnsetExternalGateway', network_ids, 'networkIds')

        # delete networks
        network_ids = [n['networkId'] for n in networks]
        post_resource(API, 'DeleteNetworks', network_ids, 'networkIds')

