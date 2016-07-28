from jsonrpc import JSONRPCResponseManager, dispatcher

import json
import socket
import itertools

class RpcServer():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 0))
        self.sock.listen(1)

    def start_serving(self):
        while True:
            connection, _ = self.sock.accept()
            try:
                while True:
                    data = connection.recv(4096).strip()
                    print("serving")
                    if data:
                        response = JSONRPCResponseManager.handle(data, dispatcher)
                        connection.send(str.encode(response.json))
                    else:
                        break
            finally:
                connection.close()
                break

    def get_sock_port(self):
        return self.sock.getsockname()[1]

class RpcClient():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 5555))
        self._id_iter = itertools.count()

    def _msg(self, name, *params):
        return dict(id = self._id_iter.__next__(),
                   params = list(params),
                   method = name)

    def call(self, method, *params):
        req = self._msg(method, *params)
        msg = json.dumps(req)
        mid = req.get('id')

        self.sock.send(str.encode(msg))

        res = self.sock.recv(4096)
        res = json.loads(bytes.decode(res))

        if res.get('id') != mid:
            raise Exception("expected id=%s, received id=%s: %s"
                            %(mid, res.get('id'), res.get('error')))

        if res.get('error') is not None:
            raise Exception(res.get('error'))

        return res.get('result')
