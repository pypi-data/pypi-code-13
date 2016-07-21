from grpc.beta.implementations import insecure_channel as create_grpc_channel
import segment_source.domain_pb2 as service
import simplejson as json

_TIMEOUT = 10

channel = create_grpc_channel('localhost', 4000)
client = service.beta_create_Source_stub(channel)

##
# Helpers
##

def _byteify(d):
    json_str = json.dumps(d)
    bytes_ = json_str.encode()

    return bytes_

##
# API
##

def set(collection, id_, properties):
    _properties = _byteify(properties)
    request = service.SetRequest(collection=collection, id=id_, properties=_properties)

    client.Set(request, _TIMEOUT)

def track(context=None, integrations=None, properties=None, anonymous_id=None,
          user_id=None, event=None):
    pass

def identify(context=None, integrations=None, traits=None, anonymous_id=None,
             user_id=None):
    pass

def group(context=None, integrations=None, traits=None, anonymous_id=None,
          user_id=None, event=None):
    pass

def keep_alive():
    pass

def get_context():
    request = service.GetContextRequest()

    try:
        response = client.GetContext(request, _TIMEOUT)
    except:
        # Hack because GetContext is kinda broken and returns errors if no context
        # is found in previous runs (last 20 runs failed || first run)
        return {}

    contents = open(response.path).read()
    context = json.loads(contents)

    return context

def store_context(payload):
    _payload = _byteify(payload)
    request = service.StoreContextRequest(payload=_payload)

    try:
        client.StoreContext(request, _TIMEOUT)
    except Exception as err:
        print(err, "Source.StoreContext failed")

def report_error(message, collection=None):
    request = service.ReportErrorRequest(message=message, collection=collection)
    client.ReportError(request, _TIMEOUT)

def report_warning(message, collection=None):
    request = service.ReportWarningRequest(message=message, collection=collection)
    client.ReportWarning(request, _TIMEOUT)
