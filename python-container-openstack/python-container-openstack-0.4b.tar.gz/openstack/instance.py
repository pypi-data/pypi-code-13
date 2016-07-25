#!/usr/bin/python
#coding=utf-8

import os
import time
import random
import subprocess
import sys

from credentials import get_nova_creds
from novaclient.client import Client

class instances:
    def __init__(self):
        self.cred		 = get_nova_creds()
        self.nova 		 = Client(**self.cred)

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get_key(self, keyname):
        self.key = keyname

    def get_flavor(self, flavorname):
        self.flavor = self.nova.flavors.find(name=flavorname)

    def get_image(self, imagename):
        self.image = self.nova.images.find(name=imagename)

    def get_networkid(self, networkname):
        for network in self.nova.networks.list():
            if network.label == networkname:
                self.network_id = network.id
                print(self.network_id)
                break

    def set_key(self, keyname):
        self.get_key(keyname)
        if not self.nova.keypairs.findall(name=self.key):
            with open(os.path.expanduser('~/Dropbox/python/key/id_rsa.pub')) as fpubkey:
                self.nova.keypairs.create(name=self.key, public_key=fpubkey.read())

    def create(self, instancename, imagename, flavorname, network_id, keyname):
        self.iname = instancename
        self.get_vm()
        self.get_flavor(flavorname)
        self.get_image(imagename)
        self.network_id = network_id
        self.set_key(keyname)
        self.instance = self.nova.servers.create(name=self.iname, image=self.image, flavor=self.flavor,
                                            key_name=self.key, nics=[{'net-id': self.network_id}])
        self.wait_instance_build()
        time.sleep(10)

    def wait_instance_build(self):
        self.get_vm()
        count = 0
        while self.vm_status == 'BUILD':
            time.sleep(10)
            # Retrieve the instance again so the status field updates
            instance = self.nova.servers.get(self.instance.id)
            self.get_vm()
            if count == 100:
                print("Timeout Create Instance")
                self.vm.delete()
                sys.exit(2)
            count += 1

    def delete(self):
        self.vm = self.nova.servers.find(name=self.iname)
        self.vm.delete()
        while True:
            if self.vm != 'notfound':
                self.get_vm()
                time.sleep(5)
            else:
                break

    def get(self, iname):
        try:
            vm = self.nova.servers.find(name=iname)
            if vm:
                return vm
        except:
            pass

    def get_fixedip(self, name):
        id = self.nova.servers.find(name=name).id
        for y in self.nova.servers.ips(id):
            self.network = y

        for x in self.nova.servers.ips(id)[self.network]:
            self.ip = x['addr']
            break
        return self.ip



if __name__ == '__main__':
    instances()