#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

from kubernetes import K8sConfig
from kubernetes import K8sPod
from kubernetes import K8sContainer
from kubernetes import K8sReplicationController
from kubernetes import K8sService
from kubernetes import K8sSecret
from openstack.ssh import ssh

import os

class kubernetes:
    def __init__(self, kubmaster):
        self.kubmaster = kubmaster
        self.connect = K8sConfig(api_host='%s:8080' % self.kubmaster)
        self.key = '~/Dropbox/python/key/id_rsa'
        self.user = 'administrator'
        self.dir = '~/Dropbox/python/pykubernetes'

    def create_pod(self, name, image, container_port=None, host_port=None):
        that_pod = K8sPod(config=self.connect, name=name)
        if container_port:
            that_pod.add_container(container=K8sContainer(name=name, image='library/%s' % image)
                                   .add_port(container_port=container_port, host_port=host_port,
                                             name=name+'port'))
        else:
            that_pod.add_container(container=K8sContainer(name=name, image='library/%s' % image))
        that_pod.create()

    def get_pod(self, name):
        that_pod = K8sPod(config=self.connect, name=name)
        that_pod.get()

    def delete_pod(self, name):
        that_pod = K8sPod(config=self.connect, name=name)
        that_pod.get()
        that_pod.delete()

    def create_replication(self, name, image, replicas):
        that_rc = K8sReplicationController(config=self.connect, name=name,
                                           image='library/%s' % image, replicas=int(replicas))
        that_rc.create()

    def get_replication(self, name):
        that_rc = K8sReplicationController(config=self.connect, name=name)
        that_rc.get()

    def delete_replication(self, name):
        exe = ssh(self.user, self.key, self.kubmaster,
                 cmd='sudo kubectl delete rc %s > /tmp/bla 2>&1' % name)
        exe.connect()

    def scale_replication(self, name, replicas):
        exe = ssh(self.user, self.key, self.kubmaster,
                  cmd='sudo kubectl scale --replicas=%s rc/%s > /tmp/bla 2>&1' % (replicas, name))
        exe.connect()

    def create_deployment(self, file=None, name=None, replicas=None):
        if file:
            exe = ssh(self.user, self.key, self.kubmaster,
                      arq='%s/deployment/%s' % (self.dir, file),
                      cmd='sudo kubectl create -f %s > /tmp/bla 2>&1' % file)
            exe.scp()
            exe.connect()
        else:
            exe = ssh(self.user, self.key, self.kubmaster,
                      cmd='sudo kubectl run %s --image=%s --replicas=%s > /tmp/bla 2>&1'
                          % (name+'-deployment', name, int(replicas)))
            exe.connect()

    def delete_deployment(self, name):
        exe = ssh(self.user, self.key, self.kubmaster,
                  cmd='sudo kubectl delete deployment %s-deployment > /tmp/bla 2>&1' % name)
        exe.connect()

    def scale_deployment(self, name, replicas):
        exe = ssh(self.user, self.key, self.kubmaster,
                  cmd='sudo kubectl scale --replicas=%s deployment/%s-deployment > /tmp/bla 2>&1'
                      % (int(replicas), name))
        exe.connect()
