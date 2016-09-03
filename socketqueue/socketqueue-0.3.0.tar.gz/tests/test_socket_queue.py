# -*- coding: utf-8 -*-

import os
import sys
import unittest
import platform
import shutil
import socket
import random

import socketqueue


def get_os():

    def get_linux_version():
        return tuple([int(i) for i in platform.uname()[2].split('-')[0].split('.')])

    def window_version():
        windows_versions = {
            '5.0' : '2k',
            '5.1' : 'xp32',
            '5.2' : 'xp64',
            '6.0' : 'vista',
            '6.1' : '7',
            '6.2' : '8'
            }
        try:
            return windows_versions['.'.join(platform.uname()[3].split('.')[:2])]
        except:
            return 'unsuported'

    def get_mac_version():
        # uname
        #('Darwin', 'HollyGolightly.local',
        #'12.2.0', 'Darwin Kernel Version 12.2.0: Sat Aug 25 00:48:52 PDT 2012;
        #root:xnu-2050.18.24~1/RELEASE_X86_64', 'x86_64', 'i386')
        # mac_ver
        #('10.8.2', ('', '', ''), 'x86_64')
        return tuple([int(i) for i in platform.mac_ver()[0].split('-')[0].split('.')])

    def get_bsd_version():
        pass

    if sys.platform in ('linux2', 'linux'):
        return ('linux',) + get_linux_version()

    elif sys.platform == 'win32':
        return ('win32',  window_version())

    elif sys.platform == 'darwin':
        return ('osx', get_mac_version())


def can_use_kqueue():
    return get_os()[0] == 'osx' and get_os[1:] > (10, 4, 0) or\
                     get_os()[0] == 'bsd'


def can_use_epoll():
    return get_os()[0] == 'linux' and get_os()[1:] >= (2, 5, 4)


class BasicSocketQueueTestCase(unittest.TestCase):
    def test_auto_select(self):
        m = socketqueue.SocketQueue()
        if sys.platform in ('linux2', 'linux'):
            if get_os()[1:] > (2, 5, 4):
                self.assertEqual(m.engine, socketqueue._SocketQueueEPoll)
            else:
                self.assertEqual(m.engine, socketqueue._SocketQueuePoll)

        elif sys.platform == 'win32':
            self.assertEqual(m.engine, socketqueue._SocketQueueSelect)

        elif sys.platform == 'darwin' or 'bsd' in sys.platform:
            self.assertEqual(m.engine, socketqueue._SocketQueueKQueue)

        else:
            self.assertEqual(m.engine, socketqueue._SocketQueuePoll)

    @unittest.skipUnless(can_use_epoll(), 'this test require linux 2.5.4 or newer')
    def test_epoll(self):
        m = socketqueue.SocketQueue(method=socketqueue.EPOLL)
        self.assertEqual(m.engine, socketqueue._SocketQueueEPoll)

    def test_select(self):
        m = socketqueue.SocketQueue(method=socketqueue.SELECT)
        self.assertEqual(m.engine, socketqueue._SocketQueueSelect)

    @unittest.skipIf(sys.platform == 'win32', "can't use poll on windows.")
    def test_poll(self):
        m = socketqueue.SocketQueue(method=socketqueue.POLL)
        self.assertEqual(m.engine, socketqueue._SocketQueuePoll)

    @unittest.skipUnless(can_use_kqueue(), 'this test requires osx or bsd')
    def test_kqueue(self):
        m = socketqueue.SocketQueue(method=socketqueue.POLL)
        self.assertEqual(m.engine, socketqueue._SocketQueueKQueue)


class NotificationTestBase(unittest.TestCase):

    def _create_socket_server(self, type='tcp'):

        import socket, random
        if type == 'tcp':

            self.socket_server = self._create_socket(type)
            while 1:
                port = random.randint(1024, 65535)
                try:

                    self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.socket_server.bind(('127.0.0.1', port))
                    self.socket_server.listen(1)
                    self.port = port
                    return self.port
                except Warning:
                    pass

        elif type == 'udp':
            self.socket_server_udp = self._create_socket(type)
            while 1:
                port = random.randint(1024, 65535)
                try:
                    self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.socket_server_udp.bind(('127.0.0.1', port))
                    self.port_udp = port
                    return port
                except Warning:
                    pass

    def _create_socket(self, type='tcp'):
        import socket
        if type == 'tcp':
            return socket.socket()
        elif type == 'udp':
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def setUp(self):
        self._create_socket_server('tcp')
        self._create_socket_server('udp')
        self.socket = self._create_socket('tcp')
        self.socket_udp = self._create_socket('udp')
        self.addr = ('127.0.0.1', self.port)
        self.addr_udp = ('127.0.0.1', self.port_udp)
        self._start_sockqueue()

    def tearDown(self):
        self.socket.close()
        self.socket_udp.close()
        self.socket_server.close()
        self.socket_server_udp.close()

    def _start_sockqueue(self):
        pass


class NotificationTestCaseGeneric(NotificationTestBase):

    def _start_sockqueue(self):
        self.sock_queue = socketqueue.SocketQueue()

    @unittest.skipIf(sys.platform == "win32", "not works on windows")
    def test_if_is_notifying_pipe(self):
        in_, out = os.pipe()
        self.sock_queue.register(in_)
        os.write(out, b"\x00")
        data = self.sock_queue.poll(1)
        self.assertEqual((in_, 1), data[0])

    def test_if_socket_server_is_notifying_tcp(self):
        self.sock_queue.register(self.socket_server)

        self.socket.connect(self.addr)
        data = self.sock_queue.poll(1)
        self.assertEqual((self.socket_server, 1), data[0])

    def test_if_socket_is_notifying_udp(self):
        self.sock_queue.register(self.socket_server_udp)
        self.socket_udp.sendto(b"test", self.addr_udp)
        data = self.sock_queue.poll(1)
        self.assertEqual((self.socket_server_udp, 1), data[0])

    def test_if_socket_is_notifying(self):

        self.socket.connect(self.addr)
        s, a = self.socket_server.accept()

        self.sock_queue.register(s)
        self.socket.send(b"data")
        data = self.sock_queue.poll(1)
        self.assertEqual((s, 1), data[0])
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        data = self.sock_queue.poll(1)
        self.assertEqual((s, 1), data[0])


@unittest.skipUnless(can_use_epoll(), 'this test require linux 2.5.4 or newer')
class NotificationTestCaseEPoll(NotificationTestCaseGeneric):
    def _start_sockqueue(self):
        self.sock_queue = socketqueue.SocketQueue(method=socketqueue.EPOLL)



@unittest.skipUnless(can_use_kqueue(), 'this test require bsd or osx')
class NotificationTestCaseKQueue(NotificationTestCaseGeneric):
    def _start_sockqueue(self):
        self.sock_queue = socketqueue.SocketQueue(method=socketqueue.KQUEUE)


@unittest.skipIf(sys.platform == 'win32', "win32 does'nt support poll")
class NotificationTestCasePoll(NotificationTestCaseGeneric):
    def _start_sockqueue(self):
        self.sock_queue = socketqueue.SocketQueue(method=socketqueue.POLL)


class NotificationTestCaseSelect(NotificationTestCaseGeneric):
    def _start_sockqueue(self):
        self.sock_queue = socketqueue.SocketQueue(method=socketqueue.SELECT)



