#!/usr/bin/env python
# encoding: utf-8
class MongoBaseObject(object):
    def change_obj_id(self, data):
        if 'id' in data:
            data['_id'] = data['id']
            del data['id']
        return data
