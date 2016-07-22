#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import json
from neutronclient.v2_0 import client
import novaclient.client as nvclient
from credentials import get_keystone_creds
from credentials import get_nova_creds

class routers:
    def __init__(self):
        self.cred = get_keystone_creds()
        self.neutron = client.Client(**self.cred)
        self.router_problem = ''
        self.prv_subnet_id = ''

    def create(self, router_name, network_id, publicname):
        self.router_name = router_name
        self.network_id = network_id

        try:
            self.neutron.format = 'json'
            # Will arrumou o set gateway para o router ter rede publica
            self.pub_net_id = self.neutron.list_networks(name=publicname)['networks'][0]['id']
            self.request = {'router': {'name': self.router_name,
                                  'external_gateway_info': {'network_id': self.pub_net_id},
                                  'admin_state_up': True}}
            self.router = self.neutron.create_router(self.request)
            self.router_id = self.router['router']['id']
            self.router = self.neutron.show_router(self.router_id)

            self.attach_network(self.router_id, self.network_id)
        except:
            print("Error Create Router")

    # Funcao do will para attach subnet no router
    def attach_network(self, router_id, network_id):
        try:
            prv_subnet_id = self.neutron.list_networks(network_id)
            for x in prv_subnet_id['networks']:
                if x['id'] == network_id:
                    self.prv_subnet_id = x['subnets'][0]
            req = {"subnet_id": self.prv_subnet_id}
            self.neutron.add_interface_router(router=router_id, body=req)
        except:
            print("Error Attach subnet router")

    def delete(self, router_id):
        self.router_id = router_id
        self.neutron.delete_router(self.router_id)

    def hastate(self, router):
        all_routers = self.neutron.list_l3_agent_hosting_routers(router)
        count_active = 0
        count_standby = 0
        count_router_up = 0
        count_router_down = 0
        # Deletando entradas repetidas no dicionario by Juliana
        ids = []
        for index, item in enumerate(all_routers['agents'], 0):
            if item['id'] not in ids:
                ids.append(item['id'])
            else:
                del all_routers['agents'][index]
        for x in all_routers['agents']:
            if x['ha_state'] == 'active':
                count_active += 1
                if not x['alive']:
                    count_router_down += 1
                else:
                    count_router_up += 1
            else:
                count_standby += 1

        if count_router_up == 0:
            print("Problem: Router active not alive (xxx): %s", router)
        else:
            if count_active == 1 and count_standby == 2:
                print("Router OK")
            else:
                print("Warning: Router UP but problem HA STATE: %s", router)

    def list_all(self):
        all_routers = []
        list = self.neutron.list_routers(retrieve_all=True)
        for x in list['routers']:
            all_routers.append(x['id'])
        return all_routers

if __name__ == '__main__':
    routers()