#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import sys
import time

from credentials import get_nova_creds
from novaclient.client import Client

class snapshots():

    def __init__(self, iname):
        self.cred = get_nova_creds()
        self.nova = Client(**self.cred)
        self.iname = iname

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get(self):
        self.id_snap = self.nova.images.find(name=self.iname).id
        self.snap_status = self.nova.images.get(self.id_snap).status

    def create(self):
        self.get_vm()
        self.vm.create_image(self.iname)
        time.sleep(5)
        self.get()
        self.check()

    def check(self):
        count = 0
        while self.snap_status != 'ACTIVE':
            time.sleep(5)
            # Retrieve the instance again so the status field updates
            self.get()
            if count == 4:
                #print('Snapshot Timeout')
                self.snap_status = 'timeout'
                break
            count += 1

    def delete(self):
        #self.get()
        if self.snap_status == 'ACTIVE':
            self.get()
            self.nova.images.delete(self.id_snap)

if __name__ == '__main__':
    snapshots()