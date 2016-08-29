import sys
import uuid
import json
import redis
import logging
import traceback


class Error(Exception):
    'Base Error Class'
    code = 0
    message = 'error'

    def __init__(self, request_message):
        self.request_message = request_message

    def to_dict(self):
        return dict(code=self.code, message=self.message, data=None)


class ParseError(Error):
    'Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.'
    code = -32700
    message = 'Parse error'


class InvalidRequestError(Error):
    'The JSON sent is not a valid Request object.'
    code = -32600
    message = 'Invalid Request'


class MethodNotFoundError(Error):
    'The method does not exist / is not available.'
    code = -32601
    message = 'Method not found'


class InvalidParamsError(Error):
    'Invalid method parameter(s).'
    code = -32602
    message = 'Invalid params'


class InternalError(Error):
    'Internal JSON-RPC error.'
    code = -32603
    message = 'Internal error'


class RpcServer(object):
    def __init__(self, redis_url: str, queue_name: str='default'):
        self.redis_server = redis.from_url(redis_url)
        self.queue_key = 'rrpc:queue:' + queue_name
        self.methods = dict()

    def _response_key(self, msg_id: str):
        if msg_id is None:
            return None
        return 'rrpc:response:{}'.format(msg_id)

    def _make_request(self, queue_key, method_name, params):
        request = dict(jsonrpc='2.0', method=method_name, params=params)
        request['id'] = str(uuid.uuid1())
        self.redis_server.rpush(queue_key, json.dumps(request))
        queue, response = self.redis_server.blpop(self._response_key(request['id']))
        response = json.loads(response.decode())
        assert response['id'] == request['id']
        if response['error'] is not None:
            raise ValueError(response['error'])
        return response['result']

    def _save_response(self, message_id, response):
        response_key = self._response_key(message_id)
        if response_key is None:
            response_key = 'rrpc:async'
        self.redis_server.rpush(response_key, json.dumps(response))
        self.redis_server.expire(response_key, 2 * 60)

    def _make_delay_request(self, queue_key, method_name, params):
        request = dict(jsonrpc='2.0', method=method_name, params=params)
        self.redis_server.rpush(queue_key, json.dumps(request))

    def _build_wrapper(self, method_name):
        def wrapper(*params):
            return self._make_request(self.queue_key, method_name, params)
        def delay_wrapper(*params):
            self._make_delay_request(self.queue_key, method_name, params)
        wrapper.delay = delay_wrapper
        return wrapper

    def _register(self, method_name, func):
        if method_name in self.methods:
            raise ValueError('{}: can not registered again'.format(method_name))
        logging.info('registering rpc method: %s', method_name)
        self.methods[method_name] = func

    def task(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            method_name = func.__name__
            self._register(method_name, func)
            return self._build_wrapper(method_name)
        else:
            def decorator(func):
                method_name = kwargs.pop('name', None) or func.__name__
                self._register(method_name, func)
                return self._build_wrapper(method_name)
            return decorator

    def dispatch(self, request):
        logging.info('receive rpc: %s', request)
        if self.methods.get(request['method']) is None:
            raise MethodNotFoundError(request)
        elif not isinstance(request['params'], (list, tuple, dict)):
            raise InvalidParamsError(request)
        params = request['params']
        try:
            if isinstance(params, dict):
                result = self.methods[request['method']](**params)
            else:
                result = self.methods[request['method']](*params)
            response = dict(jsonrpc='2.0', id=request.get('id'), result=result, error=None)
            self._save_response(request.get('id'), response)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = dict(code=1, message='RPC error', data=traceback.format_exception(exc_type, exc_value, exc_traceback))
            response = dict(jsonrpc='2.0', id=request['id'], result=None, error=error)
            self._save_response(request.get('id'), response)

    def run(self):
        logging.info('starting rpc server for %s', self.queue_key)
        while True:
            try:
                _, request = self.redis_server.blpop(self.queue_key)
                request = json.loads(request.decode())
                self.dispatch(request)
            except Error as e:
                logging.exception('RPC error')
                response = dict(jsonrpc='2.0', id=e.request_message.get('id'), result=None, error=json.dumps(e.to_dict()))
                self._save_response(e.request_message['id'], response)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.exception('Internal error')
                error = dict(code=2, message='Internal error', data=traceback.format_exception(exc_type, exc_value, exc_traceback))
                response = dict(jsonrpc='2.0', id=request.get('id'), result=None, error=error)
                self._save_response(request.get('id'), response)
