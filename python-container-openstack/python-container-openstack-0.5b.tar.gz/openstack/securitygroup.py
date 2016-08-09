#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import sys
from credentials import get_nova_creds
from novaclient.client import Client

class securitygroups():

    def __init__(self):
        self.cred = get_nova_creds()
        self.nova = Client(**self.cred)

    def create_sec(self, iname, sourceip):
        self.iname = iname
        self.sourceip = sourceip

        self.nova.security_groups.create(name=self.iname, description="Python Script")
        self.get()
        self.nova.security_group_rules.create(self.secgroup.id,
               	                       ip_protocol="icmp",
                       	               from_port=-1,
                               	       to_port=-1)
        self.nova.security_group_rules.create(self.secgroup.id,
                                              ip_protocol="tcp",
                                              from_port=22,
                                              to_port=22,
                                              cidr=self.sourceip)
        self.set()

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get(self):
        try:
            self.secgroup = self.nova.security_groups.find(name=self.iname)
            self.get_vm()
        except:
            print('Problem Security Group')
            self.get_vm()
            self.vm.delete()
            sys.exit(2)

    def set(self):
        self.get()
        self.vm.add_security_group(self.secgroup.id)

    def delete(self):
        self.get()
        self.nova.security_groups.delete(self.secgroup.id)

    def add(self, instance, group):
        vm = self.nova.servers.find(name=instance)
        secgroup = self.nova.security_groups.find(name=group)
        vm.add_security_group(secgroup.id)

    def create(self, name, protocol, port, sourceip):
        try:
            self.nova.security_groups.find(name=name)
        except:
            self.nova.security_groups.create(name=name, description=name)
            for ports in port.split(' '):
                secgroup = self.nova.security_groups.find(name=name)
                self.nova.security_group_rules.create(secgroup.id,
                                                  ip_protocol=protocol,
                                                  from_port=ports,
                                                  to_port=ports,
                                                  cidr=sourceip)

if __name__ == '__main__':
    securitygroups()