import tornado.web
from tornado.escape import json_decode, json_encode
from binascii import hexlify
import os


class Type:
    CLI = 'cli'
    REQUEST = 'request'
    THREAD = 'thread' # TODO: Implementar


class EnqueueHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            tabs = self.application.tabs
            queue = self.application.queue
            data = json_decode(self.request.body)
            process_name = data.get('processName', None)
            options = data.get('options', None)
            token = hexlify(os.urandom(5))
            if process_name in tabs:
                toenqueue = (process_name, token, options)
                queue.put(toenqueue)
            body = {'success': True, 'token': token}
            
        except ValueError:
            body = {'success': False, 'reason': NO_BODY}

        self.add_header('Content-Type', 'application/json')
        self.write(json_encode(body))

