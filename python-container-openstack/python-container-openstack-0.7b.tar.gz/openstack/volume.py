#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import sys
import time

from credentials import get_nova_creds
from novaclient.client import Client

class volumes():

    def __init__(self, iname):
        self.iname = iname
        self.cred = get_nova_creds()
        self.nova = Client(**self.cred)

    def create(self):
        try:
            self.get()
        except:
            self.nova.volumes.create(display_name=self.iname, size='2')
            time.sleep(10)
            self.get()
            pass

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get(self):
        self.get_vm()
        self.id_vol = self.nova.volumes.find(display_name=self.iname).id

    def attach(self):
        self.get()
        self.create()
        self.nova.volumes.create_server_volume(self.id_vm, self.id_vol)
        time.sleep(10)

    def delete(self):
        self.get()
        if self.vm == 'notfound':
            self.nova.volumes.delete(self.id_vol)
        else:
            self.nova.volumes.delete(self.id_vol)
            self.nova.volumes.delete_server_volume(self.id_vm, self.id_vol)

if __name__ == '__main__':
    volumes()