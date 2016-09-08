#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests
from base64 import b64encode

from goplus import mqtt

BASE_URL = "http://beta.goplusplatform.com"
MQTT_GW = "beta.goplusplatform.com"
DATA_URL = BASE_URL + "/server/income/"
IMAGE_URL = BASE_URL + "/server/getimage/"


class Thing():
    def __init__(self, did):
        self.DID = did

    def get(self, value, action):
        payload = {'did': self.DID, 'action': action, 'value': value}
        try:
            resp = requests.get(DATA_URL, params=payload)
        except requests.exceptions.RequestException as e:
            print("Error requesting: %s" % e)
            return None
        if resp:
            if resp.status_code == 200:
                return resp.json()
            else:
                print("Request error, response code %d" % resp.status_code)
                return None

    def post_image(self, binary_data):
        payload = {'did': self.DID, 'image': b64encode(binary_data)}
        try:
            resp = requests.post(IMAGE_URL, data=payload)
        except requests.exceptions.RequestException as e:
            print("Error requesting: %s" % e)
            return None
        if resp:
            if resp.status_code == 200:
                return resp.json()
            else:
                print("Request error, response code %d" % resp.status_code)
                return None

    def ack(self, value):
        return self.get(value, 'ack')

    def put(self, value):
        return self.get(value, 'put')

    def event(self):
        return self.get(None, 'event')

    def message(self, value):
        return self.get(value, 'put')


class Data(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def update(self, value):
        self.put(value)


class Geo(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def update(self, lat, lon):
        self.put("%s/%s" % (str(lat), str(lon)))


class Alert(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def update(self):
        self.event()


class Button(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def increase(self):
        self.get(None, 'inc')

    def decrease(self):
        self.get(None, 'dec')


class Message(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def update(self, message):
        self.put(message)


class Stream(Thing):
    def __init__(self, did):
        Thing.__init__(self, did)

    def update(self, image_data):
        self.post_image(image_data)

    def update_from_jpeg(self, image_filename):
        self.post_image(open(image_filename, 'rb').read())


class Level(Thing):
    def __init__(self, did, user_id, set_handler, get_handler):
        Thing.__init__(self, did)

        def handler(action, value):
            if action == 'set':
                resp = set_handler(value)
                if resp:
                    self.ack(resp)
            elif action == 'get':
                resp = get_handler()
                if resp:
                    self.ack(resp)
            else:
                print("Unknown action: %s" % action)

        self.mqtt_conn = mqtt.MQTTSub(MQTT_GW, user_id + "/thing/" + self.DID, handler)

    def start_loop(self):
        self.mqtt_conn.LoopForever()


class Switch(Thing):
    def __init__(self, did, user_id, set_on, set_off):
        Thing.__init__(self, did)

        def handler(action, value):
            if action == 'set':
                if value == "1":
                    resp = set_on()
                    if resp:
                        self.ack(1)
                elif value == "0":
                    resp = set_off()
                    if resp:
                        self.ack(0)
                else:
                    print("Unknown value: %s" % value)
            else:
                print("Unknown action: %s" % action)

        self.mqtt_conn = mqtt.MQTTSub(MQTT_GW, user_id + "/thing/" + self.DID, handler)

    def start_loop(self):
        self.mqtt_conn.LoopForever()
