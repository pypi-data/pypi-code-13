#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import os
from openstack.instance import instances
from openstack.floating import floatings
from openstack.ssh import ssh
from openstack.network import networks

class nodes:
    def __init__(self):
        self.user = 'administrator'
        self.key = '/home/dfperogil/Dropbox/id_rsa'
        self.instance = instances()
        self.network = networks()

    def create_instances(self, server, image, flavor, network_id, key_name):
        self.instance = instances()
        self.instance.create(server, image, flavor, network_id, key_name)
        self.floating = floatings(self.instance.iname)
        self.floating.create()


    def create(self, name, replicas, image, flavor, network_id, key_name):
        servers = ('%s-master %s-minion' % (name, name))
        count = 0
        for server in servers.split(' '):
            if count == 0:
                self.create_instances(server, image, flavor, network_id, key_name)
                self.ipmaster = self.instance.get_fixedip(server)
                self.install_master(floating=self.floating.ip_floating)
            else:
                for x in range(int(replicas)):
                    servername = server + str(x)
                    self.create_instances(servername, image, flavor, network_id, key_name)
                    myip = self.instance.get_fixedip(servername)
                    self.install_node(ip=myip, floating=self.floating.ip_floating)
            count += 1

    def install_master(self, floating=None):
        exe = ssh(self.user, self.key, floating,
                  arq='~/Dropbox/python/scripts/install-kubernetes-master.sh',
                  cmd='sudo bash install-kubernetes-master.sh > /tmp/bla 2>&1')
        exe.wait()
        exe.scp()
        exe.connect()

    def install_node(self, ip=None, floating=None, master=None):
        if master:
            self.ipmaster = master

        exe = ssh(self.user, self.key, floating,
                  arq='~/Dropbox/python/scripts/install-kubernetes-node.sh',
                  cmd='sudo bash install-kubernetes-node.sh > /tmp/bla 2>&1')
        exe.wait()
        exe.scp()
        exe.connect()

        files = '/etc/sysconfig/flanneld /etc/kubernetes/config /etc/kubernetes/kubelet'
        for filekub in files.split(' '):
            exe = ssh(self.user, self.key, floating,
                      cmd='sudo sed -i "s/ipmaster/%s/" %s' % (self.ipmaster, filekub))
            exe.connect()

        exe = ssh(self.user, self.key, floating,
                  cmd='sudo sed -i "s/myip/%s/" /etc/kubernetes/kubelet' % ip)
        exe.connect()

        exe = ssh(self.user, self.key, floating,
                  arq='~/Dropbox/python/scripts/restart-kubernetes-node.sh',
                  cmd='sudo bash restart-kubernetes-node.sh > /tmp/bla 2>&1')
        exe.scp()
        exe.connect()
