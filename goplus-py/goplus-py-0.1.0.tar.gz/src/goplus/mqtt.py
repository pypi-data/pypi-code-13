#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


class MQTTSub():
    def __init__(self, host, topic, message_handler):
        self.__host = host
        self.__topic = topic
        self.__handle = message_handler
        self.__connected = False

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected successfully.")
                self.__connected = True
                client.subscribe(self.__topic)
            else:
                print("Server refuse connection with code %d" % rc)

        def on_disconnect(client, userdata, rc):
            print("Lost connection to MQTT broker, trying to repair")
            client.reconnect()

        def on_message(client, userdata, message):
            str_msg = str(message.payload)
            msg_dict = dict()
            msg_list = str_msg.split(";")

            for item in msg_list:
                tmp = item.split("=")
                if len(tmp) == 2:
                    msg_dict[tmp[0]] = tmp[1]
                else:
                    print("Error in imcome msg: %s" % str_msg)
                    return

            if not msg_dict.has_key('did'):
                print("No DID in income msg: %s" % str_msg)
                return
            if not msg_dict.has_key('action'):
                print("No action in income msg: %s" % str_msg)
                return
            if not msg_dict.has_key('value'):
                print("No new value in income msg: %s" % str_msg)
                return

            self.__handle(msg_dict['action'], msg_dict['value'])

        self.__client = mqtt.Client(protocol=mqtt.MQTTv31)
        self.__client.on_connect = on_connect
        self.__client.on_disconnect = on_disconnect
        self.__client.on_message = on_message

        self.__client.connect(self.__host)

    def LoopForever(self):
        self.__client.loop_forever()

    def LoopStart(self):
        self.__client.loop_start()

    def LoopStop(self):
        self.__client.loop_stop(force=False)
