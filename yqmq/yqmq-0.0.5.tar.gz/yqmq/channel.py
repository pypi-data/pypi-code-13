# -*- coding: utf-8 -*-

# author: cainbit

import gevent.event
import gevent.queue

from yqmq.consumer import Consumer
from yqmq.consumer import Delivery
from yqmq.frame import *
from yqmq.spec import *


class Channel(object):
    def __init__(self, connection, number):
        self.conn = connection
        self.number = number
        self.consumers = {}
        self.recv_queue = gevent.queue.Queue()

    def dispatch_frame(self, frame):
        if isinstance(frame, MethodFrame) and self._handle_method(frame.method):
            return
        self.recv_queue.put(frame)

    def _wait_method_frame(self, method_class):
        frame = self.recv_queue.get()
        if not isinstance(frame, MethodFrame):
            return
        if not isinstance(frame.method, method_class):
            return
        return frame.method

    def _handle_method(self, method):
        handler_name = '_on_method_%s' % method.name
        handler = getattr(self, handler_name, None)
        if handler and callable(handler):
            gevent.spawn(handler, method)
            return True

    def open(self):
        """
        Open the channel.

        Block current concurrent until the ChannelOpenOkMethod frame is received.
        :return:
        """
        method = ChannelOpenMethod()
        self.conn.send_frame(MethodFrame(self.number, method))
        self._wait_method_frame(ChannelOpenOkMethod)

    def close(self, reply_code=0, reply_text=None):
        """
        Close the channel.

        :param reply_code:
        :param reply_text:
        :return:
        """
        reply_text = reply_text or 'Normal Shutdown'
        method = ChannelCloseMethod(reply_code, reply_text, 0, 0)
        self.conn.send_frame(MethodFrame(self.number, method))
        self._wait_method_frame(ChannelCloseOkMethod)


    def basic_consume(self, consumer_callback,
                      queue='',
                      no_ack=False,
                      exclusive=False,
                      consumer_tag=None,
                      arguments=None):
        method = BasicConsumeMethod(queue=queue,
                                    no_ack=no_ack,
                                    exclusive=exclusive,
                                    consumer_tag=consumer_tag,
                                    arguments=arguments)
        self.conn.send_frame(MethodFrame(self.number, method))
        method = self._wait_method_frame(BasicConsumeOkMethod)
        if not method:
            pass

        consumer = Consumer(method.consumer_tag, consumer_callback)
        gevent.spawn(consumer.loop)
        self.consumers[method.consumer_tag] = consumer

    def basic_cancel(self,
                     consumer_tag='',
                     nowait=False):
        pass

    def basic_ack(self, delivery_tag, multiple=False):
        method = BasicAckMethod(delivery_tag=delivery_tag,
                                multiple=multiple)
        self.conn.send_frame(MethodFrame(self.number, method))

    def basic_publish(self,
                      exchange,
                      routing_key,
                      body,
                      properties=None,
                      mandatory=False,
                      immediate=False):
        """

        :param exchange:
        :param routing_key:
        :param body:
        :param properties:
        :param mandatory:
        :param immediate:
        :return:
        """
        method = BasicPublishMethod(exchange=exchange,
                                    routing_key=routing_key,
                                    mandatory=mandatory,
                                    immediate=immediate)
        self.conn.send_frame(MethodFrame(self.number, method))

        properties = properties or BasicProperties()
        self.conn.send_frame(HeaderFrame(self.number, len(body), properties))
        limit = self.conn.params.frame_max - FRAME_HEADER_LEN
        while body:
            fragment, body = body[:limit], body[limit:]
            self.conn.send_frame(BodyFrame(self.number, fragment))

    def basic_get(self, queue='', no_ack=False):
        pass

    def basic_nack(self,
                   delivery_tag=None,
                   multiple=None,
                   requeue=True):
        pass

    def basic_qos(self,
                  prefetch_size=0,
                  prefetch_count=0,
                  all_channels=False):
        pass

    def basic_reject(self, delivery_tag, requeue=True):
        pass

    def basic_recover(self, requeue=False):
        pass

    def queue_declare(self,
                      queue='',
                      passive=False,
                      durable=False,
                      exclusive=False,
                      auto_delete=False,
                      nowait=False,
                      arguments=None):
        """
        Declare queue.

        :param queue:
        :type queue: str
        :param bool passive: Only check whether the queue exists
        :param bool durable: Survive reboots or the broker
        :param bool exclusive: Only allow access by the current connection
        :param bool auto_delete: Delete after consumer cancles or disconnects
        :param bool nowait: Don't wait for a queue_declare_ok
        :param dict arguments:
        :return:
        """
        method = QueueDeclareMethod(0, queue, passive, durable, exclusive,
                                    auto_delete, nowait, arguments)
        frame = MethodFrame(self.number, method)
        self.conn.send_frame(frame)
        self._wait_method_frame(QueueDeclareOkMethod)

    def queue_delete(self, queue=''):
        pass

    def queue_purge(self, queue='', nowait=False):
        pass

    def queue_unbind(self,
                     queue='',
                     exchange=None,
                     routing_key=None,
                     arguments=None):
        pass

    def tx_commit(self):
        pass

    def tx_rollback(self):
        pass

    def tx_select(self):
        pass

    def _on_method_basic_deliver(self, method):
        consumer = self.consumers.get(method.consumer_tag)
        if not consumer:
            pass

        header_frame = self.recv_queue.get()
        body_size = header_frame.body_size
        bodies = []
        if body_size > 0:
            body_frame = self.recv_queue.get()
            body_size -= len(body_frame.fragment)
            bodies.append(body_frame.fragment)
        body = ''.join(bodies)

        delivery = Delivery(method, header_frame.properties, body)
        consumer.recv_queue.put(delivery)
