# -*- coding: utf-8 -*-

# author: cainbit

import gevent
import gevent.queue


class Delivery(object):
    def __init__(self, method, properties, body):
        self.method = method
        self.properties = properties
        self.body = body


class Consumer(object):
    def __init__(self, tag, callback):
        self.tag = tag
        self.callback = callback
        self.recv_queue = gevent.queue.Queue()

    def loop(self):
        while 1:
            delivery = self.recv_queue.get()
            self.callback(delivery.method, delivery.properties, delivery.body)
