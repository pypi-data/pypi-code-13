#
# Autogenerated by Thrift Compiler (0.9.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:json,utf8strings
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import concord.internal.thrift.MutableEphemeralStateService
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface(concord.internal.thrift.MutableEphemeralStateService.Iface):
  def updateTopology(self, topology):
    """
    Parameters:
     - topology
    """
    pass

  def updateSchedulerAddress(self, e):
    """
    Parameters:
     - e
    """
    pass

  def registerWithScheduler(self, meta):
    """
    Parameters:
     - meta
    """
    pass


class Client(concord.internal.thrift.MutableEphemeralStateService.Client, Iface):
  def __init__(self, iprot, oprot=None):
    concord.internal.thrift.MutableEphemeralStateService.Client.__init__(self, iprot, oprot)

  def updateTopology(self, topology):
    """
    Parameters:
     - topology
    """
    self.send_updateTopology(topology)
    self.recv_updateTopology()

  def send_updateTopology(self, topology):
    self._oprot.writeMessageBegin('updateTopology', TMessageType.CALL, self._seqid)
    args = updateTopology_args()
    args.topology = topology
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_updateTopology(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = updateTopology_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.e is not None:
      raise result.e
    return

  def updateSchedulerAddress(self, e):
    """
    Parameters:
     - e
    """
    self.send_updateSchedulerAddress(e)
    self.recv_updateSchedulerAddress()

  def send_updateSchedulerAddress(self, e):
    self._oprot.writeMessageBegin('updateSchedulerAddress', TMessageType.CALL, self._seqid)
    args = updateSchedulerAddress_args()
    args.e = e
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_updateSchedulerAddress(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = updateSchedulerAddress_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.e is not None:
      raise result.e
    return

  def registerWithScheduler(self, meta):
    """
    Parameters:
     - meta
    """
    self.send_registerWithScheduler(meta)

  def send_registerWithScheduler(self, meta):
    self._oprot.writeMessageBegin('registerWithScheduler', TMessageType.ONEWAY, self._seqid)
    args = registerWithScheduler_args()
    args.meta = meta
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

class Processor(concord.internal.thrift.MutableEphemeralStateService.Processor, Iface, TProcessor):
  def __init__(self, handler):
    concord.internal.thrift.MutableEphemeralStateService.Processor.__init__(self, handler)
    self._processMap["updateTopology"] = Processor.process_updateTopology
    self._processMap["updateSchedulerAddress"] = Processor.process_updateSchedulerAddress
    self._processMap["registerWithScheduler"] = Processor.process_registerWithScheduler

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_updateTopology(self, seqid, iprot, oprot):
    args = updateTopology_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = updateTopology_result()
    try:
      self._handler.updateTopology(args.topology)
    except BoltError, e:
      result.e = e
    oprot.writeMessageBegin("updateTopology", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_updateSchedulerAddress(self, seqid, iprot, oprot):
    args = updateSchedulerAddress_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = updateSchedulerAddress_result()
    try:
      self._handler.updateSchedulerAddress(args.e)
    except BoltError, e:
      result.e = e
    oprot.writeMessageBegin("updateSchedulerAddress", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_registerWithScheduler(self, seqid, iprot, oprot):
    args = registerWithScheduler_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.registerWithScheduler(args.meta)
    return


# HELPER FUNCTIONS AND STRUCTURES

class updateTopology_args:
  """
  Attributes:
   - topology
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'topology', (TopologyMetadata, TopologyMetadata.thrift_spec), None, ), # 1
  )

  def __init__(self, topology=None,):
    self.topology = topology

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.topology = TopologyMetadata()
          self.topology.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('updateTopology_args')
    if self.topology is not None:
      oprot.writeFieldBegin('topology', TType.STRUCT, 1)
      self.topology.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.topology)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class updateTopology_result:
  """
  Attributes:
   - e
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'e', (BoltError, BoltError.thrift_spec), None, ), # 1
  )

  def __init__(self, e=None,):
    self.e = e

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.e = BoltError()
          self.e.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('updateTopology_result')
    if self.e is not None:
      oprot.writeFieldBegin('e', TType.STRUCT, 1)
      self.e.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.e)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class updateSchedulerAddress_args:
  """
  Attributes:
   - e
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'e', (Endpoint, Endpoint.thrift_spec), None, ), # 1
  )

  def __init__(self, e=None,):
    self.e = e

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.e = Endpoint()
          self.e.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('updateSchedulerAddress_args')
    if self.e is not None:
      oprot.writeFieldBegin('e', TType.STRUCT, 1)
      self.e.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.e)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class updateSchedulerAddress_result:
  """
  Attributes:
   - e
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'e', (BoltError, BoltError.thrift_spec), None, ), # 1
  )

  def __init__(self, e=None,):
    self.e = e

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.e = BoltError()
          self.e.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('updateSchedulerAddress_result')
    if self.e is not None:
      oprot.writeFieldBegin('e', TType.STRUCT, 1)
      self.e.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.e)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class registerWithScheduler_args:
  """
  Attributes:
   - meta
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'meta', (ComputationMetadata, ComputationMetadata.thrift_spec), None, ), # 1
  )

  def __init__(self, meta=None,):
    self.meta = meta

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.meta = ComputationMetadata()
          self.meta.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('registerWithScheduler_args')
    if self.meta is not None:
      oprot.writeFieldBegin('meta', TType.STRUCT, 1)
      self.meta.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.meta)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
