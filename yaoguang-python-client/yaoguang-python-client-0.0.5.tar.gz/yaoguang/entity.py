

from thriftpy.rpc import make_client
from thriftpy import load

from pkg_resources import resource_filename

import json

CONTACT=1
COMPANY=2
AD=3

class Entities(object):

    def __init__(self, address, port=9196):
        thrift = load(resource_filename(__name__, "static/yaoguang.thrift"), module_name="yaoguang_thrift")
        self._client = make_client(thrift.ThriftInterface, address, port)

    def bj_tags_ready(self):
        result = self._client.isReady("hello")
        json.loads(result)

    def get_company(self, id, fields=[]):
        asJson = self._client.get(COMPANY, fields, [id])
        return json.loads(asJson).get(id)

    def get_ad(self, id, fields=[]):
        asJson = self._client.get(AD, fields, [id])
        return json.loads(asJson).get(id)
    
    def get_ads(self, ids, fields=[]):
        asJson = self._client.get(AD, fields, ids)
        return json.loads(asJson)

    def get_contact(self, id, fields=[]):
        asJson = self._client.get(CONTACT, fields , [id])
        return json.loads(asJson).get(id)

    def get_contacts(self, ids, fields=[]):
        asJson = self._client.get(CONTACT, fields , ids)
        return json.loads(asJson)
