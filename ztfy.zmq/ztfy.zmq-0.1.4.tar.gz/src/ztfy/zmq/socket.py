#
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'


# import standard library

# import interfaces

# import packages
import zmq


def zmq_socket(address, socket_type=zmq.REQ, linger=0, protocol='tcp'):
    """Get ØMQ socket"""
    context = zmq.Context()
    socket = context.socket(socket_type)
    socket.setsockopt(zmq.LINGER, linger)
    socket.connect('{0}://{1}'.format(protocol, address))
    return socket


def zmq_response(socket, flags=zmq.POLLIN, timeout=10):
    """Get response from given socket"""
    poller = zmq.Poller()
    poller.register(socket, flags)
    if poller.poll(timeout * 1000):
        return socket.recv_json()
    else:
        return [503, "Connection timeout"]
