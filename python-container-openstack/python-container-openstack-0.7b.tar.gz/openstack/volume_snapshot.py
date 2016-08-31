#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import sys
import time

from credentials import get_nova_creds
from novaclient.client import Client

class volume_snapshots():

    def __init__(self, iname, idvol):
        self.cred = get_nova_creds()
        self.nova = Client(**self.cred)
        self.iname = iname
        self.id_vol = idvol

    def delete(self, id_vol_snap):
        self.nova.volume_snapshots.delete(id_vol_snap)

    def get_vm(self):
        try:
            self.vm = self.nova.servers.find(name=self.iname)
            self.id_vm = self.nova.servers.find(name=self.iname).id
            self.vm_status = self.nova.servers.find(name=self.iname).status
        except:
            self.vm = 'notfound'
            pass

    def get(self):
        self.vol_snap_status = self.nova.volume_snapshots.find(id=self.id_vol_snap).status

    def create(self):
        try:
            self.id_vol_snap = self.nova.volume_snapshots.create(self.id_vol).id
            time.sleep(5)
            self.check()
        except Exception as e:
            print('Problem Snapshot Volumes')
            self.get_vm()
            self.delete()
            sys.exit(2)

    def check(self):
        self.get()
        count = 0
        while self.vol_snap_status != 'available':
            time.sleep(5)
            # Retrieve the instance again so the status field updates
            self.get()
            print(self.vol_snap_status)
            if count == 5:
                print('Volume Snapshot Timeout')
                self.get_vm()
                self.vm.delete()
                sys.exit(2)
                break
            count += 1

if __name__ == '__main__':
    volume_snapshots()