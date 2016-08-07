#!/usr/bin/python
import pika
connection=pika.BlockingConnection(pika.ConnectionParameters(host="172.21.5.34"))
channel=connection.channel()
channel.queue_declare(queue="request")
channel.basic_publish(exchange="",routing_key="request",body="NetworkTopology")
print ("[X] sent hello world....")
connection.close()
