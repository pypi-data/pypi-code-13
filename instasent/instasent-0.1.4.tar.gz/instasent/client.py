import json
import requests


class Client(object):
    rootEndpoint = 'https://api.instasent.com/'
    secureChannel = 'https://api.instasent.com/'
    useSecureChannel = True

    def __init__(self, token, use_secure_channel=True):
        self.token = token
        self.useSecureChannel = use_secure_channel

    def send_sms(self, sender, to, text, client_id=''):
        if self.useSecureChannel:
            url = self.secureChannel + 'sms/'
        else:
            url = self.rootEndpoint + 'sms/'

        http_method = 'POST'

        data = {'from': sender, 'to': to, 'text': text}

        return self.execute_request(url, http_method, data)

    def get_sms_by_id(self, id):
        if self.useSecureChannel:
            url = self.secureChannel + 'sms/' + id
        else:
            url = self.rootEndpoint + 'sms/' + id

        http_method = 'GET'

        return self.execute_request(url, http_method)

    def get_sms(self, page=1, per_page=10):
        if self.useSecureChannel:
            url = self.secureChannel + 'sms/?page=' + str(page) + 'per_page=' + str(per_page)
        else:
            url = self.rootEndpoint + 'sms/?page=' + str(page) + 'per_page=' + str(per_page)

        http_method = 'GET'

        return self.execute_request(url, http_method)

    def request_verify(self, sender, to, text, token_length='', timeout='', client_id=''):
        url = self.secureChannel + 'verify/' if self.useSecureChannel else self.rootEndpoint + 'verify/'
        http_method = 'POST'
        data = {'sms': {'from': sender, 'to': to, 'text': text}}

        if client_id != '':
            data['clientId'] = client_id

        if token_length != '':
            data['tokenLength'] = token_length

        if timeout != '':
            data['timeout'] = timeout

        return self.execute_request(url, http_method, data)

    def check_verify(self, id, token):
        url = self.secureChannel + 'verify/' + id if self.useSecureChannel else self.rootEndpoint + 'verify/' + id
        url += '?token=' + token
        http_method = 'GET'

        return self.execute_request(url, http_method, {})

    def get_verify_by_id(self, id):
        url = self.secureChannel + 'verify/' + id if self.useSecureChannel else self.rootEndpoint + 'verify/' + id
        http_method = 'GET'

        return self.execute_request(url, http_method, {})

    def get_verify(self, page=1, per_page=10):
        if self.useSecureChannel:
            url = self.secureChannel + 'verify/?page=' + str(page) + 'per_page=' + str(per_page)
        else:
            url = self.rootEndpoint + 'verify/?page=' + str(page) + 'per_page=' + str(per_page)

        http_method = 'GET'

        return self.execute_request(url, http_method)

    def do_lookup(self, to):
        url = self.secureChannel + 'lookup/' if self.useSecureChannel else self.rootEndpoint + 'lookup/'
        http_method = 'POST'
        data = {'to': to}

        return self.execute_request(url, http_method, data)

    def get_lookup_by_id(self, id):
        url = self.secureChannel + 'lookup/' + id if self.useSecureChannel else self.rootEndpoint + 'lookup/' + id
        http_method = 'GET'

        return self.execute_request(url, http_method, {})

    def get_lookups(self, page=1, per_page=10):
        if self.useSecureChannel:
            url = self.secureChannel + 'lookup/?page=' + str(page) + 'per_page=' + str(per_page)
        else:
            url = self.rootEndpoint + 'lookup/?page=' + str(page) + 'per_page=' + str(per_page)
        http_method = 'GET'

        return self.execute_request(url, http_method, {})

    def get_account_balance(self):
        url = self.secureChannel + 'organization/account/' if self.useSecureChannel else self.rootEndpoint + 'organization/account/'
        http_method = 'GET'

        return self.execute_request(url, http_method, {})

    def execute_request(self, url='', http_method='', data=''):
        headers = {'Authorization': 'Bearer ' + self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

        if http_method == 'GET':
            response = requests.get(url, headers=headers)
        elif http_method == 'POST':
            response = requests.post(url, data=json.dumps(data), headers=headers)

        return {'response_body': response.json(), 'response_code': response.status_code}

