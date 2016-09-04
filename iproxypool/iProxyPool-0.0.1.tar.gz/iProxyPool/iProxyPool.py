#-*- coding=utf-8 -*-

'''
Created On Sep 2, 2016

@author: enming.zhang
'''

import socket

SERVER_IP = '139.196.254.213'
#SERVER_IP = '127.0.0.1'
SERVER_PORT = 7777

class ProxyPoolClient(object):
    def __init__(self):
        self.sock_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conn_to_server(self):
        self.sock_instance.connect((SERVER_IP, SERVER_PORT))

    def get_proxy(self, num):
        req_str = ''
        req_proxy_str = ''
        req_proxy_list = []
        if num < 10:
            req_str = 'R_0' + str(num)
        elif num in range(10, 100):
            req_str = 'R_' + str(num)
        else:
            print 'Number of requirment is not in range!'

        self.sock_instance.send(req_str)
        req_proxy_str = self.sock_instance.recv(27 * num)
        req_proxy_list = req_proxy_str.split(',')

        return req_proxy_list

    def exit_to_server(self):
        self.sock_instance.send('exit')
        self.sock_instance.close()


soc_handle = ProxyPoolClient()

def ConnectToProxyPool():
    soc_handle.conn_to_server()


def ReqProxy(req_num):
    return soc_handle.get_proxy(req_num)


def ReleaseConnect():
    soc_handle.exit_to_server()