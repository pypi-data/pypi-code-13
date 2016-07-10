import json
import os
import requests
from requests.auth import HTTPBasicAuth

from dp8 import DP8Meta

_CONFIGURATION_TEMPLATES_FOLDER = 'vdirect_configuration_templates'

_PAYLOAD_TEMPLATE = {
    "parameters": {
        "beanName": "__REPLACE__", "projection": "__REPLACE__", "indexEntries": "__REPLACE__"
    },
    "deviceConnections": {
        "defensePro": [{"deviceId": {"name": "__REPLACE__"}}]
    }
}

_READ_CONFIG_TEMPLATE_NAME = '__dp_read_client__.vm'


class DPClient(object):
    def __init__(self, vdirect_ip, dp_device_id, vdirect_user="vDirect", vdirect_pwd="radware"):
        self.vdirect_ip = vdirect_ip
        self.dp_device_id = dp_device_id
        self.vdirect_user = vdirect_user
        self.vdirect_pwd = vdirect_pwd
        self.auth = HTTPBasicAuth(self.vdirect_user, self.vdirect_pwd)
        self._upload_templates_if_needed()
        self.config_templates = []

    def read(self, bean_name, projection=[], index_entries=[], filter_func=None):
        payload = _PAYLOAD_TEMPLATE.copy()
        payload['parameters']['beanName'] = bean_name
        payload['parameters']['projection'] = projection
        payload['parameters']['indexEntries'] = index_entries
        payload['deviceConnections']['defensePro'][0]['deviceId']['name'] = self.dp_device_id
        r = requests.post('http://%s:2188/api/template/%s' % (self.vdirect_ip, _READ_CONFIG_TEMPLATE_NAME),
                          data=json.dumps(payload),
                          headers={'Content-Type': 'application/vnd.com.radware.vdirect.template-parameters+json'},
                          auth=self.auth)
        if r.status_code != 200:
            raise Exception('Read operation failed with status code %d. Reason: %s' % (r.status_code, r.text))
        else:
            data = json.loads(r.json()['parameters']['result'])
            return filter(filter_func, data) if filter_func else data


    def _upload_templates_if_needed(self):
        config_templates = os.listdir('./%s' % _CONFIGURATION_TEMPLATES_FOLDER)
        for config_template in config_templates:
            r = requests.get('http://%s:2188/api/template/%s' % (self.vdirect_ip, config_template), auth=self.auth)
            if r.status_code not in [200, 404]:
                raise Exception('Reading template failed with status code %d. Reason: %s' % (r.status_code, r.text))
            if r.status_code == 404:
                config_template_path = os.getcwd() + os.sep + _CONFIGURATION_TEMPLATES_FOLDER + os.sep + config_template
                self.config_templates.append(config_template_path)
                with open(config_template_path, 'r') as f:
                    data = f.read()
                r = requests.post('http://%s:2188/api/template/?name=%s' % (self.vdirect_ip, config_template),
                                  data=data,
                                  headers={'Content-Type': 'text/x-velocity'},
                                  auth=self.auth)
                if r.status_code != 201:
                    raise Exception(
                        'Uploading template failed with status code %d. Reason: %s' % (r.status_code, r.text))

    def __del__(self):
        for config_template in self.config_templates:
            requests.delete('http://%s:2188/api/template/%s' % (self.vdirect_ip, config_template), auth=self.auth)

