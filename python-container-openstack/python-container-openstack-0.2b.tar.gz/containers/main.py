#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'


from docker import Client
import subprocess
import time

class container:
    def __init__(self):
        self.cli = Client(base_url='unix://var/run/docker.sock')
        self.status = ''

    def getip(self, name):
        value = self.cli.inspect_container(name)
        self.ip = value['NetworkSettings']['IPAddress']

    def delete(self, name):
        try:
            self.cli.stop(name)
            self.cli.remove_container(name)
        except Exception as e:
            print(e)

    def create(self, name, image):
        try:
            self.cli.create_container(image, name=name)
        except Exception as e:
            print(e)

    def check_image(self, name):
        check = self.cli.images(name=name)
        if not check:
            self.status = 'NOT'
        else:
            self.status = 'OK'
        return self.status

    def wait_build(self, name):
        self.check_image(name)
        count = 0
        value = 60
        while count < value:
            if self.status != 'OK':
                time.sleep(10)
                count += 1
                self.check_image(name)
            else:
                break

            if count == value:
                print('wait_build timeout 10min')
                break

    def build(self, name, dockerfile):
        try:
            subprocess.Popen(['docker build -t %s %s > /tmp/bla.txt' % (name, dockerfile)],
                                      shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            self.check_image(name)
        except Exception as e:
            print(e)

    def build_compose(self, name, dockerfile):
        try:
            subprocess.Popen(['eval $(docker-machine env --swarm %s) && docker-compose up -d %s > /tmp/bla.txt' % (name, dockerfile)],
                                      shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            self.check_image(name)
        except Exception as e:
            print(e)

    def image_delete(self, name):
        try:
            self.cli.remove_image(name)
        except Exception as e:
            print(e)

    def image_problem(self):
        list_all = self.cli.containers(all=True)
        for x in list_all:
            if x['State'] == 'exited':
                self.cli.remove_container(x['Id'])

if __name__ == '__main__':
    container()
