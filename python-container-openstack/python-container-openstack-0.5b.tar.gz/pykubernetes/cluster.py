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
        self.kubnodes_ip = []
        self.kubnodes_name = []
        self.ipmaster = ''

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
                vm = self.instance.get(server)
                if not vm:
                    self.create_instances(server, image, flavor, network_id, key_name)
                    ip_floating = self.floating.ip_floating
                    self.install_master(floating=ip_floating)
                else:
                    floating = floatings(server)
                    ip_floating = floating.getip(server)
                self.ipmaster = self.instance.get_fixedip(server)
                self.ipmaster_floating = ip_floating
            else:
                for x in range(int(replicas)):
                    servername = server + str(x)
                    vm = self.instance.get(servername)
                    if not vm:
                        self.create_instances(servername, image, flavor, network_id, key_name)
                        ip_floating = self.floating.ip_floating
                        myip = self.instance.get_fixedip(servername)
                        self.install_node(ip=myip, floating=ip_floating)
                    myip = self.instance.get_fixedip(servername)
                    self.kubnodes_ip.append(myip)
                    self.kubnodes_name.append(servername)
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
