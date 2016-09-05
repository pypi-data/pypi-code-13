import json
import os

import redis
import time


class RedisConnection(object):

    def __init__(self, host=None, port=6379):
        if host is not None:
            self.redis = redis.StrictRedis(host=host, port=port, db=5)
            self.redis.delete('all-pipelines')
        else:
            self.redis = None

    def running(self, id, trigger=None):
        if self.redis is None:
            return
        status = self.redis.get(id)
        status = json.loads(status.decode('ascii'))
        status.update({
            'id': id,
            'running': True,
            'started': time.time(),
            'trigger': trigger
        })
        self.redis.set(id, json.dumps(status))

    def idle(self, id, success, reason=None):
        if self.redis is None:
            return
        status = self.redis.get(id)
        status = json.loads(status.decode('ascii'))
        status.update({
            'id': id,
            'running': False,
            'ended': time.time(),
            'success': success,
            'reason': reason
        })
        if success is True:
            status['last_success'] = status['ended']
        self.redis.set(id, json.dumps(status, ensure_ascii=True))

    def register(self, id):
        if self.redis is None:
            return
        self.redis.sadd('all-pipelines', id)
        if self.redis.get(id) is None:
            status = {
                'id': id,
                'running': False
            }
            self.redis.set(id, json.dumps(status, ensure_ascii=True))

    def all_statuses(self):
        if self.redis is None:
            return []
        all_ids = self.redis.smembers('all-pipelines')
        pipe = self.redis.pipeline()
        for id in all_ids:
            pipe.get(id)
        return [json.loads(sts.decode('ascii')) for sts in pipe.execute()]

status = RedisConnection(os.environ.get('DATAPIPELINES_REDIS_HOST'))