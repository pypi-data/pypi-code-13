#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

import subprocess
import re

class main:
    def command(self, iface=False):
        self.iface = iface
        self.ifconfig = subprocess.Popen(["ip a s %s" %self.iface],
                                        shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self.route = subprocess.Popen(["ip r s"],
                                        shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

    def get(self, regexp, location, ip=False, route=False):
        if route:
            cmd = self.route.stdout
        else:
            cmd = self.ifconfig.stdout
        for line in cmd:
            result = re.findall(regexp, line)
            if result:
                inet = list(line.split(' '))
                if ip:
                    inet = inet[location].split('/')
                    self.value = inet[0]
                    return self.value
                self.value = inet[location]
                return self.value

    def getip(self, iface):
        self.command(iface)
        self.get('inet ', 5, ip=True)
        self.ip = self.value

    def getmac(self, iface):
        self.command(iface)
        self.get('link/ether ', 5)
        self.mac = self.value

    def getroute(self):
        self.command()
        self.get('default ', 2, route=True)
        self.route = self.value

        hostname = socket.gethostname()
        print(hostname)

        full_hostname = socket.getfqdn()
        print(full_hostname)

    def get_iface(self, username, key, ip):
        iface = subprocess.check_output('ssh -l %s -i %s %s '
                                        '"ip route show | grep -i default" | awk \'{print $NF}\''
                                        %(username, key, ip), shell=True).replace('\n', '')
        return iface

if __name__ == '__main__':
    inet()