#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import os
import time
from docker import Client

class containers:
    def __init__(self, remote):
        self.remote = remote
        self.cli = Client(base_url='unix://var/run/docker.sock')

    def create(self, name, image, args=None):
        try:
            check = os.system('eval $(docker-machine env %s) && '
                            'docker ps -a | grep %s$ > /dev/null 2>&1' % (self.remote, name))
            if check != 0:
                if args:
                    os.system('eval $(docker-machine env %s) && docker run -d %s -ti --name %s %s'
                                    % (self.remote, args, name, image))
                else:
                    os.system('eval $(docker-machine env %s) && docker run -d -ti --name %s %s'
                              % (self.remote, name, image))
                time.sleep(10)
            os.system('eval $(docker-machine env %s) && docker start '
                            '%s > /dev/null 2>&1' % (self.remote, name))
        except Exception as e:
            print e.message

    def delete(self, name):
        try:
            os.system('eval $(docker-machine env %s) && docker stop %s' % (self.remote, name))
            time.sleep(5)
            os.system('eval $(docker-machine env %s) && docker rm %s' % (self.remote, name))
        except Exception as e:
            print e.message

    def delete_image(self, name):
        try:
            os.system('eval $(docker-machine env %s) && docker rmi -f %s' % (self.remote, name))
        except Exception as e:
            print e.message

    def build(self, name, dockerfile):
        try:
            check = os.system('eval $(docker-machine env %s) && '
                              'docker images | grep ^%s > /dev/null 2>&1' % (self.remote, name))
            if check != 0:
                os.system('eval $(docker-machine env %s) && docker build '
                      '-t %s %s > /tmp/bla.txt 2>&1' % (self.remote, name, dockerfile))
                #self.wait_build(name)
        except Exception as e:
            print e.message

    def start(self, name):
        os.system('eval $(docker-machine env %s) && docker start %s' % (self.remote, name))
        time.sleep(5)

if __name__ == '__main__':
    containers()