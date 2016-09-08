#based Andy Barilla's hover.py gist on github --> https://gist.github.com/bassburner/b0dd93e71ff18303c059

import requests
import json

class HoverException(Exception):
    pass

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
content_type = 'application/json;charset=UTF-8'
referer = 'https://www.hover.com/signin'

class HoverAPI(object):
    def __init__(self, username, password):
        self.refresh = False
        self.dns_records = None
        r = requests.get('https://www.hover.com')
        self.session_cookie = 'hover_session=%s; '%(r.cookies['hover_session'])
        headers = {
            'user-agent': user_agent, 
            'content-type': content_type, 
            'referer': referer,
            'cookie': self.session_cookie
        }
        params = {"username": username, "password": password}
        r = requests.post("https://www.hover.com/signin/auth.json", headers=headers, params=params)
        self.cookies = {"hoverauth": r.cookies["hoverauth"]}
        #self.getDnsByDomain()
    
    def getDnsByDomain(self):
        if not self.refresh:
            self.dns_records = client.call("get", "dns")
        return self.dns_records

    def call(self, method, resource, data=None):
        url = "https://www.hover.com/api/{0}".format(resource)
        r = requests.request(method, url, data=data, cookies=self.cookies)
        if not r.ok:
            raise HoverException(r)
        if r.content:
            body = r.json()
            if "succeeded" not in body or body["succeeded"] is not True:
                raise HoverException(body)
            return body


if __name__ == '__main__':
    # connect to the API using your account
    client = HoverAPI("hover_user_id", "hover_password")  
    #data = client.getDnsByDomain()
    #print data.get('domains')  
    ## get details of a domains without DNS records
    print client.call("get", "domains")
    ## get all domains and DNS records
    #zclient.call("get", "dns")
    ## notice the "id" field of domains in response to the above calls - that's needed
    ## to address the domains individually, like so:
    ## get details of a specific domain without DNS records
    #client.call("get", "domains/dom123456")
    ## get DNS records of a specific domain:
    #client.call("get", "domains/dom123456/dns")
    ## create a new A record:
    #record = {"name": "mysubdomain", "type": "A", "content": "127.0.0.1"}
    #client.call("post", "domains/dom123456/dns", record)
    ## create a new SRV record
    ## note that content is "{priority} {weight} {port} {target}"
    #record = {"name": "mysubdomain", "type": "SRV", "content": "10 10 123 __service"}
    #client.call("post", "domains/dom123456/dns", record)
    ## create a new MX record
    ## note that content is "{priority} {host}"
    #record = {"name": "mysubdomain", "type": "MX", "content": "10 mail"}
    #client.call("post", "domains/dom123456/dns", record)
    ## notice the "id" field of DNS records in the above calls - that's
    ##  needed to address the DNS records individually, like so:
    ## update an existing DNS record
    #client.call("put", "dns/dns1234567", {"content": "127.0.0.1"})
    ## delete a DNS record:
    #client.call("delete", "dns/dns1234567") 