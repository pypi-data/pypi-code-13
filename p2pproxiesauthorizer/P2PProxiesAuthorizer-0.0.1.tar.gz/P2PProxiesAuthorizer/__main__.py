import urllib3
import argparse
import json

class P2PProxiesAuthorizer:
    def __init__(self):
        self.ip_provider = 'http://www.httpbin.org/ip'
        self.api_base = 'http://rev-api.proxies.online'
        self.api_login = '/login/login'
        self.api_check_login = '/login/check'
        self.api_add = '/account/ips/ip/add'
        self.http = urllib3.PoolManager()

        self.parse_args()
        self.login(self.email, self.password)
        self.add_ip(self.get_remote_ip())

    def parse_args(self):
        parser = argparse.ArgumentParser(description='P2PProxiesAuthorizer')
        parser.add_argument('-e', required=True, type=str, help='E-mail')
        parser.add_argument('-p', required=True, type=str, help='Password')

        args = parser.parse_args()
        self.email = args.e
        self.password = args.p

    def get_remote_ip(self):
        r = self.http.request('GET', 'http://www.httpbin.org/ip')
        j = json.loads(r.data.decode('utf-8'))
        return str(j['origin'])

    def login(self, email, password):
        r = self.http.request('POST',
                              '{0}{1}'.format(self.api_base, self.api_login),
                              fields={'email': email, 'password': password})
        self.cookie = r.headers['Set-Cookie']
        print(r.data)

    def add_ip(self, ip):
        r = self.http.request('POST',
                              '{0}{1}'.format(self.api_base, self.api_add),
                              fields={'ip': ip},
                              headers={'Cookie': self.cookie})
        print(r.data)


if __name__ == "__main__":
    main = P2PProxiesAuthorizer()