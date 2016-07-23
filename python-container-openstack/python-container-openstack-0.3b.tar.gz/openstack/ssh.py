#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import subprocess
import sys
import os
import time

class ssh():

    def __init__(self, username, key, host, arq=None, cmd=None):
        self.username = username
        self.key = key
        self.command = cmd
        self.host = host
        self.file = arq

    def scp(self):
        try:
            self.wait()
            os.system('scp -i %s -o StrictHostKeyChecking=no '
                      '-o UserKnownHostsFile=/dev/null %s %s@%s: > /dev/null 2>&1'
                      % (self.key, self.file, self.username, self.host))
        except:
            print("Problem SCP")

    def connect(self):
        try:
            self.wait()
            os.system('ssh -tt -o StrictHostKeyChecking=no '
                      '-o UserKnownHostsFile=/dev/null %s@%s -i %s %s > /dev/null 2>&1'
                      % (self.username, self.host, self.key, self.command))
        except:
            print("Problem SSH")

    def check(self):
        self.status = os.system('ssh -i %s -o StrictHostKeyChecking=no '
                                '-o UserKnownHostsFile=/dev/null '
                                '%s@%s %s > /dev/null 2>&1'
                                % (self.key, self.username, self.host, 'date'))
        return self.status

    def wait(self):
        self.check()
        if self.status != 0:
            count = 0
            while count < 30:
                print('wait ssh')
                if self.status == 0:
                    break
                time.sleep(10)
                count += 1
                self.check()
                if count == 30:
                    print('Problem Connect SSH')
                    exit()

if __name__ == '__main__':
    ssh()