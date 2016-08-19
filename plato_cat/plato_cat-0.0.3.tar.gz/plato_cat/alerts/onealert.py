import requests
import json


class OneAlert(object):

    def call(self, exceptions):
        url = 'http://api.110monitor.com/alert/api/event'
        payload = json.dumps({
            "app": "bcc67cab-afab-8259-6f86-42402abc52ab",
            "eventId": "12345",
            "eventType": "trigger",
            "alarmName": "FAILURE for production/HTTP",
            "entityName": "host-192.168.0.253",
            "entityId": "host-192.168.0.253",
            "priority": 1,
            "alarmContent": {
                "ping time": "2500ms",
                "load avg": 0.75
            }
        })
        requests.post(url, payload)
