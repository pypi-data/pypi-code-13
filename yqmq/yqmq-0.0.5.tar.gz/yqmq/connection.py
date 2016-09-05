# -*- coding: utf-8 -*-

# author: cainbit

import socket

import gevent
import gevent.queue

from yqmq.channel import Channel
from yqmq.frame import *
from yqmq.spec import *

CHANNEL_MAX_NUM = 32768


class ConnectionParameters(object):
    """
    Parameters for connection
    """
    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 5672)
        self.username = kwargs.get('username', 'guest')
        self.password = kwargs.get('password', 'guest')
        self.vhost = kwargs.get('vhost', '/')
        self.channel_max = 0
        self.frame_max = 0
        self.heartbeat = 0


class Connection(object):
    """
    The connection class provides methods for a client to establish a
    network connection to a server.
    """

    _client_properites = {
        'product': 'yqmq',
        'capabilities': {
            'authentication_failure_close': True,
            'basic.nack': True,
            'connection.blocked': True,
            'consumer_cancel_notify': True,
            'publisher_confirms': True,
        },
    }

    def __init__(self, params):
        self.params = params
        self.sock = None
        self.buf = ''
        self.heartbeat = None
        self.channels = {}
        self.send_queue = gevent.queue.Queue()
        self.recv_queue = gevent.queue.Queue()

    @property
    def closed(self):
        """whether the connection is closed"""
        return self.sock.closed

    def connect(self):
        """connect to server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.params.host, self.params.port))
        gevent.spawn(self._recv_loop)
        gevent.spawn(self._send_loop)
        self._handshake()

    def close(self):
        """close the channel"""
        if not self.closed:
            self.sock.close()

    def send_frame(self, frame):
        """send frame to mq server"""
        self.send_queue.put(frame)

    def _recv_loop(self):
        buf = ''
        payload_size = None
        frame_size = None
        while 1:
            try:
                data = self.sock.recv(4096)
            except:
                data = None
            if not data:
                self.close()
                break
            buf += data
            while 1:
                if payload_size is None:
                    if len(buf) >= FRAME_HEADER_LEN:
                        payload_size = struct.unpack("!I", buf[3:FRAME_HEADER_LEN])[0]
                        frame_size = FRAME_HEADER_LEN + payload_size + 1
                if payload_size is not None and len(buf) >= frame_size:
                    frame = decode_frame(buf[:frame_size])
                    buf = buf[frame_size:]
                    payload_size = None
                    g = gevent.spawn(self._dispatch_frame, frame)
                else:
                    break
        del buf

    def _send_loop(self):
        while 1:
            frame = self.send_queue.get()
            payload = frame.pack()
            try:
                self.sock.sendall(payload)
            except:
                self.close()
                break

    def _dispatch_frame(self, frame):
        if not frame.channel_num:
            if isinstance(frame, HeartbeatFrame):
                return
            if not self._handle_method(frame.method):
                self.recv_queue.put(frame)
        else:
            channel = self.channels.get(frame.channel_num)
            if channel:
                channel.dispatch_frame(frame)
            else:
                pass

    def _wait_method_frame(self, method_class):
        frame = self.recv_queue.get()
        if not isinstance(frame, MethodFrame):
            return
        if not isinstance(frame.method, method_class):
            return
        return frame.method

    def _handle_method(self, method):
        """handle method frame"""
        handler_name = '_on_method_%s' % method.name
        handler = getattr(self, handler_name, None)
        if handler and callable(handler):
            gevent.spawn(handler, method)
            return True

    def _start_heartbeat(self):
        """start to send heartbeat"""
        def _send_heartbeat():
            gevent.spawn(self.send_frame, HeartbeatFrame())

        self.heartbeat = gevent.get_hub().loop.timer(0, self.params.heartbeat)
        self.heartbeat.start(_send_heartbeat)

    def _handshake(self):
        self.sock.sendall(PROTOCOL_HEADER)
        method = self._wait_method_frame(StartMethod)
        if not method:
            pass
        self._handle_method_start(method)

        method = self._wait_method_frame(TuneMethod)
        if not method:
            pass
        self._handle_method_tune(method)

        method = self._wait_method_frame(ConnectionOpenOkMethod)
        if not method:
            pass
        self._handle_method_connection_open_ok(method)

    def channel(self, number=None):
        """
        create a new channel with the next available channel number or pass
        in a channel number to use.
        """
        if len(self.channels) == self.params.channel_max:
            return None

        if number is None:
            for number in xrange(0, self.params.channel_max):
                number += 1
                if number not in self.channels:
                    break
        if number > self.params.channel_max:
            # todo: raise an exception
            return None
        channel = Channel(self, number)
        self.channels[number] = channel
        channel.open()
        return channel

    def _handle_method_start(self, method):
        """handle method start frame"""
        response = '\0%s\0%s' % (self.params.username, self.params.password)
        method = StartOkMethod(client_properties=self._client_properites,
                               response=response)
        self.send_frame(MethodFrame(0, method))

    def _handle_method_tune(self, method):
        """handle method tune frame"""
        self.params.channel_max = method.channel_max or CHANNEL_MAX_NUM
        self.params.frame_max = method.frame_max
        self.params.heartbeat = method.heartbeat
        self._start_heartbeat()

        method = TuneOkMethod(self.params.channel_max, self.params.frame_max, self.params.heartbeat)
        self.send_frame(MethodFrame(0, method))
        method = ConnectionOpenMethod(virtual_host=self.params.vhost, insist=True)
        self.send_frame(MethodFrame(0, method))

    def _handle_method_connection_open_ok(self, method):
        """handle method connection frame"""
        pass
