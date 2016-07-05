from jsonrpc import JSONRPCResponseManager, dispatcher
import json
import socket, asyncore
import itertools

class RpcHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(4096).strip()
        response = JSONRPCResponseManager.handle(data, dispatcher)
        self.send(str.encode(response.json))

class RpcServer(asyncore.dispatcher):
    def __init__(self, host):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, 0))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        handler = RpcHandler(sock)

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
        id = req.get('id')

        self.sock.send(str.encode(msg))

        res = self.sock.recv(4096)
        res = json.loads(bytes.decode(res))

        if res.get('id') != id:
            raise Exception("expected id=%s, received id=%s: %s"
                            %(id, res.get('id'), res.get('error')))

        if res.get('error') is not None:
            raise Exception(res.get('error'))

        return res.get('result')
