#!/usr/bin/env python
#coding=utf-8
import getopt
import os
import sys
import time

from mitmproxy import proxy

from FriedRing import FriedRing


def main():
    opts, args = getopt.getopt(sys.argv[1:], "hp:w:")
    strPort=8888
    fnamescript='__crisschan_TEMP'+str(time.time())
    for op, value in opts:
        if op == "-p":
            strPort = value
        elif op == "-w":
            fnamescript = value
        elif op == "-h":
            #usage()
            print '-p the proxy port\r\n-w the script_solution  name'
            sys.exit()
    print 'the proxy port is :'+str(strPort)
    config = proxy.ProxyConfig(
        cadir=os.path.expanduser("~/.mitmproxy/"),
        port=int(strPort)
    )
    server = proxy.ProxyServer(config)
    m = FriedRing(server, fnamescript)
    m.run()

if __name__ == "__main__":
    main()