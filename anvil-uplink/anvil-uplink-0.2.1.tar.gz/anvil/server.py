from __future__ import unicode_literals
import threading, time, json, random, string, sys, traceback, numbers

from ws4py.client.threadedclient import WebSocketClient

import anvil

__author__ = 'Meredydd Luff <meredydd@anvil.works>'

_url = 'wss://anvil.works/uplink'

def _gen_id():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))


### The following code is kept in sync between server-side and uplink-side Python code.
### It is synchronised manually at the moment; this should change

class LiveObjectProxy(anvil.LiveObject):

    def __init__(self,spec):
        for k in ["itemCache", "iterItems"]:
            if spec.get(k, {}) is None:
                del spec[k]
        anvil.LiveObject.__init__(self, spec)

    def __getattr__(self, item):
        if item in self._spec["methods"]:
            def item_fn(*args, **kwargs):
                lo_call = dict(self._spec)
                lo_call["method"] = item
                return _do_call(args, kwargs, lo_call=lo_call)

            return item_fn
        else:
            raise AttributeError(item)

    def __getitem__(self, item):
        if item in self._spec.get("itemCache", {}):
            return self._spec["itemCache"][item]

        getitem = self.__getattr__("__getitem__")
        return getitem(item)

    def __setitem__(self, key, value):
        if key in self._spec.get("itemCache", {}):
            del self._spec["itemCache"][key]

        setitem = self.__getattr__("__setitem__")
        r = setitem(key, value)

        if "itemCache" in self._spec and (isinstance(value, str) or isinstance(value, numbers.Number) or isinstance(value, bool) or value is None):
            self._spec["itemCache"][key] = value

        return r

    class Iter:
        def __init__(self, live_object):
            self._lo_call = dict(live_object._spec)
            self._lo_call["method"] = "__anvil_iter_page__";

            i = live_object._spec.get("iterItems", {})
            self._idx = 0
            self._items = i.get("items", None)
            self._next_page = i.get("nextPage", None)

        def _fetch_state(self):
            r = _do_call([self._next_page], {}, lo_call=self._lo_call)
            self._items = r["items"]
            self._next_page = r.get("nextPage", None)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._items is None:
                self._fetch_state()

            if self._idx < len(self._items):
                r = self._items[self._idx]
                self._idx += 1
                return r

            if self._next_page is None:
                raise StopIteration

            self._items = None
            return self.next()

        def __next__(self):
            return self.next()

    def __iter__(self):
        if "__anvil_iter_page__" in self._spec["methods"]:
            return LiveObjectProxy.Iter(self)
        else:
            raise Exception("Not iterable: <LiveObject: %s>" % self._spec.get("backend", "INVALID"))

    def __len__(self):
        if "__len__" in self._spec["methods"]:
            return self.__getattr__("__len__")()
        else:
            l = 0
            for _ in self.__iter__():
                l += 1
            return l



class LazyMedia(anvil.Media):
    def __init__(self, spec):
        if isinstance(spec,LazyMedia):
            spec = spec._spec
        self._spec = spec
        self._details = None
        self._fetched = None

    def _fetch(self):
        if self._details is None:
            self._fetched = call("fetch_lazy_media", self._spec)
        return self._fetched

    def _get(self, key, attr=None):
        if attr is None:
            attr = key
        return self._spec[key] if key in self._spec else getattr(self._fetch(), attr)

    def get_name(self):
        return self._get("name")

    def get_content_type(self):
        return self._get("mime-type", "content_type")

    def get_length(self):
        return self._get("length")

    def get_bytes(self):
        return self._fetch().get_bytes()


class AnvilWrappedError(Exception):
    def __init__(self, value):
        self.extra_data = value
        self.value = ""
        self.wrapped_python_stack = False
        if "message" in value:
            self.value = value["message"]
        if "type" in value and value["type"] == "exception":
            self.value = value["data"]["msg"]
            self.wrapped_python_stack = True

    def __str__(self):
        return repr(self.value)


def _report_exception(id=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.extract_tb(exc_traceback)

    msg = str(exc_type.__name__) + ": " + str(exc_value)
    trace = [(filename.replace("\\","/"), lineno) for (filename, lineno, _, _) in tb]
    trace.reverse()
    p = trace.pop() # Remove the bottom stack frame from the traceback

    if isinstance(exc_value, AnvilWrappedError) and exc_value.wrapped_python_stack:
        msg = exc_value.extra_data["data"]["msg"]
        trace = exc_value.extra_data["data"]["trace"] + trace
    elif isinstance(exc_value, SyntaxError):
        msg = "SyntaxError: %s" % exc_value.text
        trace.insert(0, (exc_value.filename, exc_value.lineno))

    return {
        "error": {
            "type": "exception",
            "data": {
                "msg": msg,
                "trace": trace
            },
            "message": "Python error"
        },
        "id": id
    }


def fill_out_media(json, handle_media_fn):
    obj_descr = []
    path = []

    def do_fom(json):
        if isinstance(json, dict):
            for i in json:
                path.append(i)
                json[i] = do_fom(json[i])
                path.pop()
        elif isinstance(json, list) or isinstance(json, tuple):
            json = list(json)
            for i in range(len(json)):
                path.append(i)
                json[i] = do_fom(json[i])
                path.pop()
        elif isinstance(json, LazyMedia):
            d = dict(json._spec)
            d["path"] = list(path)
            obj_descr.append(d)
            json = None
        elif isinstance(json, anvil.Media):
            extra = handle_media_fn(json)
            d = {"type": ["DataMedia"], "path": list(path), "mime-type": json.content_type, "name": json.name}
            if extra is not None:
                d.update(extra)
            obj_descr.append(d)
            json = None
        elif isinstance(json, anvil.LiveObject):
            #print "Serialising LiveObject: " + repr(json._spec) + " at " + repr(path)
            obj_descr.append({"type": ["LiveObject"], "path": list(path), "live-object": json._spec})
            json = None

        return json

    json = do_fom(json)
    json["objects"] = obj_descr
    return json


def _reconstruct_objects(json, reconstruct_data_media):
    def set_in_path(obj, path, payload):
        last_obj = None
        key = None
        for k in path:
            last_obj = obj
            key = k
            obj = obj[k]

        if last_obj is not None:
            last_obj[key] = payload

    if "objects" in json:
        for d in json["objects"]:

            reconstructed = None

            for t in d["type"]:
                if t == "DataMedia":
                    reconstructed = reconstruct_data_media(d)
                    break

                elif t == "LazyMedia":
                    reconstructed = LazyMedia(d)
                    break

                elif t == "LiveObject":
                    reconstructed = LiveObjectProxy(d["live-object"])
                    break

            if reconstructed is not None:
                set_in_path(json, d["path"], reconstructed)
            else:
                raise Exception("Server module cannot accept an object of type '"+d["type"][0]+"'")

        del json["objects"]
    return json
### end common code



class StreamingMedia(anvil.Media):
    def __init__(self, content_type, name):
        self._content_type = content_type
        self._content = b''
        self._complete = False
        self._name = name

    def add_content(self, data, last_chunk=False):
        self._content += data
        self._complete = last_chunk

    def is_complete(self):
        return self._complete

    def get_content_type(self):
        return self._content_type

    def get_bytes(self):
        return self._content

    def get_url(self):
        raise None

    def get_name(self):
        return self._name



def mk_live_object(spec):
    return _backends.get(spec["backend"], LiveObjectProxy)(spec)



class _IncomingReqResp:
    def __init__(self, json):
        self.media = {}

        def reconstruct_data_media(d):
            reconstructed = StreamingMedia(d['mime-type'], d.get("name", None))
            self.media[d['id']] = reconstructed
            return reconstructed

        self.json = _reconstruct_objects(json, reconstruct_data_media)

        _incoming_requests[self.json["id"]] = self
        self.maybe_execute()

    def add_binary_data(self, json, data):
        self.media[json['mediaId']].add_content(data, json['lastChunk'])
        if json['lastChunk']:
            self.maybe_execute()

    def is_ready(self):
        for id in self.media:
            if not self.media[id].is_complete():
                return False
        return True

    def maybe_execute(self):
        if not self.is_ready():
            return

        del _incoming_requests[self.json["id"]]

        self.execute()


class _IncomingRequest(_IncomingReqResp):
    def execute(self):

        def make_call():
            _call_info.stack_id = self.json.get('call-stack-id', None)
            try:
                if 'liveObjectCall' in self.json:
                    loc = self.json['liveObjectCall']
                    spec = dict(loc)

                    if self.json["id"].startswith("server-"):
                        spec["source"] = "server"
                    elif self.json["id"].startswith("client-"):
                        spec["source"] = "client"
                    else:
                        spec["source"] = "UNKNOWN"

                    del spec["method"]
                    backend = loc['backend']
                    inst = _backends[backend](spec)
                    method = inst.__getattribute__(loc['method'])
                    r = method(*self.json['args'], **self.json['kwargs'])
                else:
                    r = _registrations[self.json['command']](*self.json["args"], **self.json["kwargs"])

                _get_connection().send_reqresp({"id": self.json["id"], "response": r})
            except:
                _get_connection().send_reqresp(_report_exception(self.json["id"]))

        threading.Thread(target=make_call).start()


class _IncomingResponse(_IncomingReqResp):
    def execute(self):
        id = self.json['id']
        if id in _call_responses:
            _call_responses[id] = self.json
            with _waiting_for_calls:
                _waiting_for_calls.notifyAll()
        else:
            print("Got a response for an unknown ID: " + repr(self.json))

# requestId->_IncomingRequest
_incoming_requests = {}


class LocalCallInfo(threading.local):
    def __init__(self):
        self.stack_id = None


_call_info = LocalCallInfo()

_connection = None
_connection_lock = threading.Lock()

_registrations = {}
_backends = {}

_fatal_error = None

def reconnect(closed_connection):
    global _connection
    with _connection_lock:
        if _connection != closed_connection:
            return
        _connection = None

    def retry():
        time.sleep(1)
        print("Reconnecting...")
        _get_connection()

    try:
        for k in _call_responses.keys():
            if _call_responses[k] is None:
                _call_responses[k] = {'error': 'Connection to server lost'}

        with _waiting_for_calls:
            _waiting_for_calls.notifyAll()

    finally:
        threading.Thread(target=retry).start()


class _Connection(WebSocketClient):
    def __init__(self):
        print("Connecting to " + _url)
        WebSocketClient.__init__(self, _url)

        self._ready_notify = threading.Condition()
        self._ready = False
        self._next_chunk_header = None
        self._sending_lock = threading.RLock()

    def is_ready(self):
        return self._ready

    def wait_until_ready(self):
        with self._ready_notify:
            while not self._ready:
                self._ready_notify.wait()

    def _signal_ready(self):
        self._ready = True
        with self._ready_notify:
            self._ready_notify.notifyAll()

    def opened(self):
        print("Anvil websocket open")
        self.send(json.dumps({'key': _key, 'v':2}))
        for r in _registrations.keys():
            self.send(json.dumps({'type': 'REGISTER', 'name': r}))
        for b in _backends.keys():
            self.send(json.dumps({'type': 'REGISTER_LIVE_OBJECT_BACKEND', 'backend': b}))

    def closed(self, code, reason=None):
        print("Anvil websocket closed (code %s, reason=%s)" % (code, reason))
        self._signal_ready()
        reconnect(self)

    def received_message(self, message):
        global _fatal_error

        if message.is_binary:
            hdr = self._next_chunk_header
            _incoming_requests[hdr['requestId']].add_binary_data(hdr, message.data)
            self._next_chunk_header = None

        else:
            data = json.loads(message.data.decode())

            type = data["type"] if 'type' in data else None

            if 'auth' in data:
                print("Authenticated OK")
                self._signal_ready()
            elif 'output' in data:
                print("Anvil server: " + data['output'].rstrip("\n"))
            elif type == "CALL":
                _IncomingRequest(data)
            elif type == "CHUNK_HEADER":
                self._next_chunk_header = data
            elif type is None and "id" in data:
                _IncomingResponse(data)
            elif type is None and "error" in data:
                _fatal_error = data["error"]
                print("Fatal error from Anvil server: " + str(_fatal_error))
            else:
                print("Anvil websocket got unrecognised message: "+repr(data))

    def send(self, payload, binary=False):
        with self._sending_lock:
            return WebSocketClient.send(self, payload, binary)

    def send_reqresp(self, reqresp):
        if not self._ready:
            raise RuntimeError("Websocket connection not ready to send request")

        media = []

        def enqueue_media(m):
            media_id = _gen_id()
            media.append((media_id, m))
            return {"id": media_id}

        reqresp = fill_out_media(reqresp, enqueue_media)

        self.send(json.dumps(reqresp))

        for (id,m) in media:
            data = m.get_bytes()
            l = len(data)
            i = 0
            n = 0
            while i < l:
                chunk_len = min(l - i, 10000)
                with self._sending_lock:
                    self.send(json.dumps({'type': 'CHUNK_HEADER', 'requestId': reqresp['id'], 'mediaId': id,
                                          'chunkIndex': n, 'lastChunk': (i + chunk_len == l)}))
                    self.send(data[i:(i+chunk_len)], True)
                i += chunk_len
                n += 1


_key = None


def _get_connection():
    global _connection

    if _key is None:
        raise Exception("You must use anvil.server.connect(key) before anvil.server.call()")

    with _connection_lock:
        if _connection is None:
            _connection = _Connection()
            _connection.connect()
            _connection.wait_until_ready()
    return _connection


def connect(key, url='wss://anvil.works/uplink'):
    global _key, _url, _fatal_error
    _key = key
    _url = url
    _fatal_error = None # Reset because of reconnection attempt
    _get_connection()


def run_forever():
    while True:
        time.sleep(1)


# can be used as a decorator too
def register(fn, name=None):
    if isinstance(fn, str):
        # Someone's using the old syntax. Our bad.
        (fn, name) = (name, fn)

    if name is None:
        name = fn.__name__

    _registrations[name] = fn

    if _connection is not None and _connection.is_ready():
        _connection.send_reqresp({'type': 'REGISTER', 'name': name})

    return fn

callable = register


def register_live_object_backend(cls):

    name = "uplink." + cls.__name__
    _backends[name] = cls

    if _connection is not None and _connection.is_ready():
        _connection.send_reqresp({'type': 'REGISTER_LIVE_OBJECT_BACKEND', 'backend': name})

    return cls

live_object_backend = register_live_object_backend


# A parameterised decorator
def callable_as(name):
    return lambda f: register(f, name)


_call_responses = {}
_waiting_for_calls = threading.Condition()

def _do_call(args, kwargs, fn_name=None, lo_call=None): # Yes, I do mean args and kwargs without *s
    if _fatal_error is not None:
        raise Exception("Anvil fatal error: " + str(_fatal_error))

    c = _get_connection()

    id = _gen_id()

    _call_responses[id] = None

    with _waiting_for_calls:
        #print("Call stack ID = " + repr(_call_info.stack_id))
        req = {'type': 'CALL', 'id': id, 'args': args, 'kwargs': kwargs,
               'call-stack-id': _call_info.stack_id}

        if fn_name:
            req["command"] = fn_name
        elif lo_call:
            req["liveObjectCall"] = lo_call
        else:
            raise Exception("Expected one of fn_name or lo_call")

        c.send_reqresp(req)

        while _call_responses[id] == None:
            _waiting_for_calls.wait()

    r = _call_responses.pop(id)

    if 'response' in r:
        return r['response']
    if 'error' in r:
        raise AnvilWrappedError(r["error"])
    else:
        raise Exception("Bogus response from server: " + repr(r))



def call(fn_name, *args, **kwargs):
    return _do_call(args, kwargs, fn_name=fn_name)

def wait_forever():
    _get_connection()
    while True:
        try:
            if _fatal_error is not None:
                raise Exception("Anvil fatal error: " + str(_fatal_error))
            call("anvil.private.echo", "keep-alive")
            time.sleep(30)
        except:
            if _fatal_error is None:
                print("Anvil uplink disconnected; attempting to reconnect in 10 seconds.")
                # Give ourselves a chance to reconnect
                time.sleep(10)
                print("Reconnecting...")
