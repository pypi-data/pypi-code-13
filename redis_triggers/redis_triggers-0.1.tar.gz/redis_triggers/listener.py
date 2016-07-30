from django.conf import settings
import time
import json
import redis
import threading
#from exceptions import MandatoryParamsNotSpecified

class Listener(threading.Thread):
    def __init__(self, r, channels, func_class):
        threading.Thread.__init__(self)
        self.redis = r
        self.redis.config_set('notify-keyspace-events', 'Kx')
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        func_class.dispatch()
        self.dispatcher = func_class.dispatcher
        self.func_class = func_class

    def __json__(self):
        try:
            return json.loads(self.function_data)
        except TypeError as ex:
            return dict()

    def __contains__(self):
        try:
            if self.function_data.get('function_name') and self.function_data.get('params'):
                return True
            return False
        except AttributeError as ex:
            return False

    def __del__(self):
        self.redis.delete(self.key)
        return True

    def __work__(self, item):
        #print item['channel'], ":i", item['data']
        if item['data'] == '1' or item['data'] == 1:
            pass
        else:
            self.key = item['channel'].split(':')[-1]
            self.function_data = self.redis.get(self.key)
            self.__del__()
            self.function_data = self.__json__()
            if self.__contains__():
                func = self.dispatcher.__getitem__(self.function_data.__getitem__('function_name'))
                func(**self.function_data.__getitem__('params'))
            else:
                pass
                '''
                raise MandatoryParamsNotSpecified(MANDATORY_PARAMS_NOT_SPECIFIED, \
                                                MANDATORY_PARAMS_NOT_SPECIFIED, \
                                                __name__)
                '''

    def run(self):
        #self.redis.setex('autokey', 'simply', 20)
        for item in self.pubsub.listen():
            if item.get('data') == 'KILL':
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            self.__work__(item)

class Interface(object):
    ''''''
    def __init__(self, r):
        self.redis = r

    def set(self, function_name, params, expiry):
        data = {
            'function_name': function_name,
            'params': params
        }
        timestamp = int(time.time())
        self.redis.set(timestamp, json.dumps(data))
        self.redis.setex(function_name + ':' + str(timestamp), '', expiry)
        return True

