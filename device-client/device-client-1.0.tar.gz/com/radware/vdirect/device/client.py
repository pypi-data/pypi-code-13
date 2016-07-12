import json
import os
from operator import itemgetter

import requests
from requests.auth import HTTPBasicAuth


_CONFIGURATION_TEMPLATES_FOLDER = 'vdirect_configuration_templates'

_PAYLOAD_TEMPLATE = {
    "parameters": {
        "query": {"beanName": "__REPLACE__", "projection": "__REPLACE__", "indexEntries": "__REPLACE__"}
    },
    "deviceConnections": {
        "device": [{"deviceId": {"name": "__REPLACE__"}}]
    }
}


def get_client(vdirect_ip, device_id, vdirect_user="vDirect", vdirect_pwd="radware"):
    auth = HTTPBasicAuth(vdirect_user, vdirect_pwd)
    r = requests.get('http://%s:2188/api/defensePro/%s' % (vdirect_ip, device_id),
                     auth=auth)
    if r.status_code == 200:
        return DPClient(vdirect_ip, device_id, vdirect_user, vdirect_pwd)
    else:
        r = requests.get('http://%s:2188/api/appwall/%s' % (vdirect_ip, device_id),
                         auth=auth)
        if r.status_code == 200:
            return AppwallClient(vdirect_ip, device_id, vdirect_user, vdirect_pwd)
        else:
            return AlteonClient(vdirect_ip, device_id, vdirect_user, vdirect_pwd)


class Client(object):
    def __init__(self, vdirect_ip, device_id, template_name, vdirect_user, vdirect_pwd):
        self.vdirect_ip = vdirect_ip
        self.device_id = device_id
        self.template_name = template_name
        self.vdirect_user = vdirect_user
        self.vdirect_pwd = vdirect_pwd
        self.auth = HTTPBasicAuth(self.vdirect_user, self.vdirect_pwd)
        self.config_templates = []
        self._upload_templates_if_needed()

    def read(self, bean_name, projection=[], index_entries=[], filter_func=None, sort_key=None):
        if sort_key and sort_key not in projection:
            projection.append(sort_key)
        payload = _PAYLOAD_TEMPLATE.copy()
        payload['parameters']['query']['beanName'] = bean_name
        payload['parameters']['query']['projection'] = projection
        payload['parameters']['query']['indexEntries'] = index_entries
        payload['deviceConnections']['device'][0]['deviceId']['name'] = self.device_id
        r = requests.post('http://%s:2188/api/template/%s' % (self.vdirect_ip, self.template_name),
                          data=json.dumps(payload),
                          headers={'Content-Type': 'application/vnd.com.radware.vdirect.template-parameters+json'},
                          auth=self.auth)
        if r.status_code != 200:
            raise Exception('Read operation failed with status code %d. Reason: %s' % (r.status_code, r.text))
        else:
            data = json.loads(r.json()['parameters']['result'])
            data = filter(filter_func, data) if filter_func else data
            return sorted(data, key=itemgetter(sort_key)) if sort_key else data


    def _upload_templates_if_needed(self):
        config_templates = os.listdir('./%s' % _CONFIGURATION_TEMPLATES_FOLDER)
        config_templates.sort()
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
        if self.config_templates:
            for config_template in self.config_templates:
                requests.delete('http://%s:2188/api/template/%s' % (self.vdirect_ip, config_template), auth=self.auth)


class DPClient(Client):
    def __init__(self, vdirect_ip, device_id, vdirect_user="vDirect", vdirect_pwd="radware"):
        super(DPClient, self).__init__(vdirect_ip, device_id, '__dp_read_client__.vm', vdirect_user, vdirect_pwd)


class AlteonClient(Client):
    def __init__(self, vdirect_ip, device_id, vdirect_user="vDirect", vdirect_pwd="radware"):
        super(AlteonClient, self).__init__(vdirect_ip, device_id, '__alteon_read_client__.vm', vdirect_user,
                                           vdirect_pwd)


class AppwallClient(Client):
    def __init__(self, vdirect_ip, device_id, vdirect_user="vDirect", vdirect_pwd="radware"):
        super(AppwallClient, self).__init__(vdirect_ip, device_id, '__appwall_read_client__.vm', vdirect_user,
                                            vdirect_pwd)

