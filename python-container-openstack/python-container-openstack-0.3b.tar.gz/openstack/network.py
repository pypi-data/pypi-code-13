#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

from neutronclient.v2_0 import client
from credentials import get_keystone_creds

class networks:
    def __init__(self):
        self.cred = get_keystone_creds()
        self.neutron = client.Client(**self.cred)

    def create(self, network_name, network_ip):
        self.network_name = network_name
        self.network_ip = network_ip

        try:
            self.body_sample = {'network': {'name': self.network_name,
                           'admin_state_up': True}}

            self.netw = self.neutron.create_network(body=self.body_sample)
            self.net_dict = self.netw['network']
            self.network_id = self.net_dict['id']
            self.body_create_subnet = {'subnets': [{'cidr': self.network_ip,
                                  'ip_version': 4, 'network_id': self.network_id,
                                  'dns_nameservers': ['8.8.8.8', '8.8.4.4']}]}

            self.subnet = self.neutron.create_subnet(body=self.body_create_subnet)
            self.subnet_id = self.subnet['subnets'][0]['id']
        except:
            print("Erro create network")

    def get(self, network_name):
        self.network_name = network_name
        self.body_value = self.neutron.list_networks()
        for x in self.body_value['networks']:
            if x['name'] == self.network_name:
                self.network_id = x['id']
                return self.network_id
            #    self.delete_ports(x['subnets'])
            #    self.delete((x['id']))

    def delete(self, network_id):
        self.network_id = network_id
        self.neutron.delete_network(self.network_id)

    def delete_ports(self, subnet_id):
        self.subnet_id = subnet_id
        self.body_value = self.neutron.list_ports()
        for x in self.body_value['ports']:
            if x['fixed_ips'][0]['subnet_id'] == self.subnet_id:
                self.neutron.delete_port(x['id'])

if __name__ == '__main__':
    networks()