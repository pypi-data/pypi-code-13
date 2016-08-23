#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import time
import os
import subprocess

from openstack.instance import instances
from openstack.floating import floatings
from openstack.securitygroup import securitygroups
from openstack.ssh import ssh

class nodes:
    def __init__(self):
        self.instance = instances()

    def validate(self, name, ip):
        check = os.system('docker-machine ls | grep %s > /dev/null 2>&1' % ip)
        if check == 0:
            status = os.system('docker-machine ls | grep %s | grep Unknown > /dev/null 2>&1' % ip)
            if status == 0:
                os.system('docker-machine ls | grep %s && docker-machine rm -f %s' % (name, name))
                check = 1
        else:
            os.system('docker-machine ls | grep %s && docker-machine rm -f %s' % (name, name))
        return check

    def instance_create(self, name, image, flavor, networkid, username, key, keyname, myip):
        try:
            self.instance.set_key(keyname)
            self.instance.create(name, image, flavor, networkid)
            time.sleep(10)
            self.floating = floatings(name)
            self.floating.create()
            securitygroup = securitygroups()
            securitygroup.create(name, 'tcp', '2376 8500', '0.0.0.0/0')
            securitygroup.add(name, name)
            time.sleep(10)
        except Exception as e:
            print e.message

    def create_registry(self, name, username, key):
        try:
            floating = floatings(name)
            ip = floating.getip(name)
            os.system('docker-machine '
                      'create -d generic --generic-ip-address %s '
                      '--generic-ssh-user %s --generic-ssh-key %s '
                      '--generic-ssh-port 22 %s' % (ip, username, key, name))
            time.sleep(20)
            os.system('eval $(docker-machine env %s) && docker run -d     '
                      '-p "8500:8500"     -h "consul"     '
                      'progrium/consul -server -bootstrap' % name)
        except Exception as e:
            print e.message

    def create_swarm_master(self, username, key, name, cluster_name):
        try:
            floating = floatings(name)
            ip = floating.getip(name)
            iface = self.get_iface(username, key, ip)
            os.system('docker-machine create -d generic --generic-ip-address %s '
                      '--generic-ssh-user %s --generic-ssh-key %s '
                      '--generic-ssh-port 22 --swarm --swarm-master '
                      '--swarm-discovery="consul://$(docker-machine ip %s):8500" '
                      '--engine-opt="cluster-store=consul://$(docker-machine ip %s):8500" '
                      '--engine-opt="cluster-advertise=%s:2376" %s'
                      % (ip, username, key, cluster_name, cluster_name, iface, name))
        except Exception as e:
            print e.message

    def create_swarm(self, username, key, name, cluster_name):
        try:
            floating = floatings(name)
            ip = floating.getip(name)
            iface = self.get_iface(username, key, ip)
            os.system('docker-machine create -d generic --generic-ip-address %s '
                      '--generic-ssh-user %s --generic-ssh-key %s '
                      '--generic-ssh-port 22 --swarm '
                      '--swarm-discovery="consul://$(docker-machine ip %s):8500" '
                      '--engine-opt="cluster-store=consul://$(docker-machine ip %s):8500" '
                      '--engine-opt="cluster-advertise=%s:2376" %s'
                      % (ip, username, key, cluster_name, cluster_name, iface, name))
        except Exception as e:
            print e.message

    def install(self, name, username, key, cluster_name=None):
        floating = floatings(name)
        ip = floating.getip(name)
        vm = self.instance.get(name)
        if not vm:
            print('instance not found')
            exit()

        check = self.validate(name, ip)
        if check != 0:
            if not cluster_name:
                os.system('docker-machine create -d generic --generic-ip-address %s '
                          '--generic-ssh-user %s --generic-ssh-key %s '
                          '--generic-ssh-port 22 %s' % (ip, username, key, name))
            else:
                self.create_swarm(username, key, name, cluster_name)

    def create_cluster(self, name, image, flavor, networkid, username, key, keyname, myip, range):
        try:
            registry = name
            names = [registry, registry+'-node-01', registry+'-node-02']
            swmaster = names[1]
            swnode = names[2]
            count = 0
            for x in names:
                vm = self.instance.get(x)
                if not vm:
                    self.instance_create(x, image, flavor, networkid, username, key, keyname, myip)

                floating = floatings(x)
                ip = floating.getip(x)

                if x == registry:
                    check = self.validate(x, ip)
                    if check != 0:
                        self.create_registry(x, username, key)
                        time.sleep(5)
                else:
                        if count == 1:
                            check = self.validate(x, ip)
                            if check != 0:
                                self.create_swarm_master(username, key, x, registry)
                                self.swarm_master = x
                                time.sleep(5)
                        else:
                            check = self.validate(x, ip)
                            if check != 0:
                                self.create_swarm(username, key, x, registry)
                                time.sleep(15)
                count += 1

            floating = floatings(swmaster)
            ip = floating.getip(swmaster)
            check = self.validate(swmaster, ip)
            if check == 0:
                self.create_network(swmaster, range)
                self.docker_run(swmaster, swmaster)

            floating = floatings(swnode)
            ip = floating.getip(swnode)
            check = self.validate(swnode, ip)
            if check == 0:
                self.docker_run(swnode, swmaster)
        except Exception as e:
            print e.message

    def create_network(self, cluster_name, range):
        try:
            os.system('eval $(docker-machine env --swarm %s) && '
                      'docker network create --driver overlay --subnet=%s internal' % (cluster_name, range))
        except Exception as e:
            print e.message

    def docker_run(self, name, cluster_name):
        os.system('eval $(docker-machine env --swarm %s) && docker run -itd --name=ubuntu14-%s --net=internal '
                  '--env="constraint:node==%s" ubuntu:14.04'
                  % (cluster_name, name, name))

    def get_iface(self, username, key, ip):
        iface = subprocess.check_output('ssh -o StrictHostKeyChecking=no '
                                        '-o UserKnownHostsFile=/dev/null -l %s -i %s %s '
                                        '"ip route show | grep -i default" | awk \'{print $NF}\''
                                        %(username, key, ip), shell=True).replace('\n', '')
        return iface

if __name__ == '__main__':
    nodes()