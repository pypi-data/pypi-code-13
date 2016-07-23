from neutronclient.v2_0 import client
import novaclient.client as nvclient
from credentials import get_keystone_creds
from credentials import get_nova_creds

class loadbalance:
    def __init__(self):
        self.cred = get_keystone_creds()
        self.neutron = client.Client(**self.cred)
        self.pool_id = ''

    def create_vip(self, protocol, protocol_port, name, pool_id, subnet_id):
        args = {"protocol": protocol,
                "protocol_port": protocol_port,
                "name": name,
                "pool_id": pool_id,
                "subnet_id": subnet_id}
        return self.neutron.create_vip({"vip": args})

    def create_pool(self, method, protocol, name, subnet_id):
        args = {"lb_method": method,
                "protocol": protocol,
                "name": name,
                "subnet_id": subnet_id}
        return self.neutron.create_pool({"pool": args})

    def get_pool(self, name):
        pools = self.neutron.list_pools()
        for x in pools['pools']:
            if name == x['name']:
                self.pool_id = x['id']
                return x['id']

    def add_member(self, protocol, ip, pool_id):
        args = {"protocol_port": protocol,
                "address": ip,
                "pool_id": pool_id}
        return self.neutron.create_member({"member": args})

if __name__ == '__main__':
    loadbalance()