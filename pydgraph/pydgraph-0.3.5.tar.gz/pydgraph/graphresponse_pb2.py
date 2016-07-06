# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graphresponse.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='graphresponse.proto',
  package='graph',
  syntax='proto3',
  serialized_pb=_b('\n\x13graphresponse.proto\x12\x05graph\"\x18\n\x07Request\x12\r\n\x05query\x18\x01 \x01(\t\":\n\x07Latency\x12\x0f\n\x07parsing\x18\x01 \x01(\t\x12\x12\n\nprocessing\x18\x02 \x01(\t\x12\n\n\x02pb\x18\x03 \x01(\t\"%\n\x08Property\x12\x0c\n\x04prop\x18\x01 \x01(\t\x12\x0b\n\x03val\x18\x02 \x01(\x0c\"w\n\x04Node\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x0b\n\x03xid\x18\x02 \x01(\t\x12\x11\n\tattribute\x18\x03 \x01(\t\x12#\n\nproperties\x18\x04 \x03(\x0b\x32\x0f.graph.Property\x12\x1d\n\x08\x63hildren\x18\x05 \x03(\x0b\x32\x0b.graph.Node\"=\n\x08Response\x12\x16\n\x01n\x18\x01 \x01(\x0b\x32\x0b.graph.Node\x12\x19\n\x01l\x18\x02 \x01(\x0b\x32\x0e.graph.Latency24\n\x06\x44graph\x12*\n\x05Query\x12\x0e.graph.Request\x1a\x0f.graph.Response\"\x00\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='graph.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='graph.Request.query', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=54,
)


_LATENCY = _descriptor.Descriptor(
  name='Latency',
  full_name='graph.Latency',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parsing', full_name='graph.Latency.parsing', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='processing', full_name='graph.Latency.processing', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pb', full_name='graph.Latency.pb', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=114,
)


_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='graph.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='prop', full_name='graph.Property.prop', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='val', full_name='graph.Property.val', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=153,
)


_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='graph.Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='graph.Node.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='xid', full_name='graph.Node.xid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attribute', full_name='graph.Node.attribute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='properties', full_name='graph.Node.properties', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='children', full_name='graph.Node.children', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=155,
  serialized_end=274,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='graph.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='n', full_name='graph.Response.n', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='l', full_name='graph.Response.l', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=337,
)

_NODE.fields_by_name['properties'].message_type = _PROPERTY
_NODE.fields_by_name['children'].message_type = _NODE
_RESPONSE.fields_by_name['n'].message_type = _NODE
_RESPONSE.fields_by_name['l'].message_type = _LATENCY
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Latency'] = _LATENCY
DESCRIPTOR.message_types_by_name['Property'] = _PROPERTY
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'graphresponse_pb2'
  # @@protoc_insertion_point(class_scope:graph.Request)
  ))
_sym_db.RegisterMessage(Request)

Latency = _reflection.GeneratedProtocolMessageType('Latency', (_message.Message,), dict(
  DESCRIPTOR = _LATENCY,
  __module__ = 'graphresponse_pb2'
  # @@protoc_insertion_point(class_scope:graph.Latency)
  ))
_sym_db.RegisterMessage(Latency)

Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), dict(
  DESCRIPTOR = _PROPERTY,
  __module__ = 'graphresponse_pb2'
  # @@protoc_insertion_point(class_scope:graph.Property)
  ))
_sym_db.RegisterMessage(Property)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), dict(
  DESCRIPTOR = _NODE,
  __module__ = 'graphresponse_pb2'
  # @@protoc_insertion_point(class_scope:graph.Node)
  ))
_sym_db.RegisterMessage(Node)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'graphresponse_pb2'
  # @@protoc_insertion_point(class_scope:graph.Response)
  ))
_sym_db.RegisterMessage(Response)


import abc
import six
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

class BetaDgraphServicer(object):
  def Query(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)

class BetaDgraphStub(object):
  def Query(self, request, timeout):
    raise NotImplementedError()
  Query.future = None

def beta_create_Dgraph_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import graphresponse_pb2
  import graphresponse_pb2
  request_deserializers = {
    ('graph.Dgraph', 'Query'): graphresponse_pb2.Request.FromString,
  }
  response_serializers = {
    ('graph.Dgraph', 'Query'): graphresponse_pb2.Response.SerializeToString,
  }
  method_implementations = {
    ('graph.Dgraph', 'Query'): face_utilities.unary_unary_inline(servicer.Query),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

def beta_create_Dgraph_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  import graphresponse_pb2
  import graphresponse_pb2
  request_serializers = {
    ('graph.Dgraph', 'Query'): graphresponse_pb2.Request.SerializeToString,
  }
  response_deserializers = {
    ('graph.Dgraph', 'Query'): graphresponse_pb2.Response.FromString,
  }
  cardinalities = {
    'Query': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'graph.Dgraph', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)
