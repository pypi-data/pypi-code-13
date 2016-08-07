#!/usr/bin/python
import pika
connection=pika.BlockingConnection(pika.ConnectionParameters(host="172.21.5.34"))
channel=connection.channel()
channel.queue_declare(queue="request")
def get_request(cn,method,properties,body):
	print("[*] get request"+body)
channel.basic_consume(get_request,queue="request",no_ack=True)
print("[x] waiting for requests....")
channel.start_consuming()
