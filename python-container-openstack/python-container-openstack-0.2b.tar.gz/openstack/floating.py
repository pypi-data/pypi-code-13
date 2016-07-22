#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import sys
from credentials import get_nova_creds
from novaclient.client import Client

class floatings():

    def __init__(self, iname):
        self.cred = get_nova_creds()
        self.nova = Client(**self.cred)
        self.iname = iname

    def create(self):
        self.get()
        self.ip_flo = self.nova.floating_ips.get(self.id_ip)
        self.ip_floating = self.nova.floating_ips.get(self.id_ip).ip
        try:
            self.get_vm()
            self.vm.add_floating_ip(self.ip_flo)
        except Exception as e:
            print e.message
            print('Problem Attach Floating')
            self.get_vm()
            self.vm.delete()
            sys.exit(2)

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get(self):
        self.floating_ip = self.nova.floating_ips.list()

        if self.floating_ip:
            x = len(self.floating_ip)
            count = 0
            for f in self.floating_ip:
                if f.fixed_ip == None:
                    self.id_ip = f.id
                    break
                else:
                    if count == x - 1:
                        f = self.nova.floating_ips.create(self.nova.floating_ip_pools.list()[0].name)
                        self.id_ip = f.id
                count += 1
        else:
            f = self.nova.floating_ips.create(self.nova.floating_ip_pools.list()[0].name)
            self.id_ip = f.id

    def getip(self, name):
        id = self.nova.servers.find(name=self.iname).id
        for x in self.nova.floating_ips.list():
            if x.instance_id == id:
                self.ip = x.ip
                return(self.ip)

if __name__ == '__main__':
    floatings()