'''This module implements the IP transport layer for PTP.

It exports the IPTransport class. Both the transport layer and the basic PTP
implementation are Vendor agnostic. Vendor extensions should extend these to
support more operations.
'''
from __future__ import absolute_import
from ..ptp import PTPError
from construct import (
    Array, Bytes, Container, Embedded, Enum, ExprAdapter, Range, Struct,
    ULInt16, ULInt32,
)
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from Queue import Queue


__all__ = ('IPTransport')
__author__ = 'Luis Mario Domenzain'

# TODO: Implement discovery mechanisms for PTP/IP like zeroconf.


class IPTransport(object, Protocol):
    '''Implement IP transport.'''
    def __init__(self, dev=None):
        '''Instantiate the first available PTP device over IP'''
        self.__setup_constructors()
        sequoia = ('192.168.47.1', 15740)
        # Establish Command/Data Connection.
        # Establish Event Connection.
        self.__event_queue = Queue()

    # Helper methods.
    # ---------------------
    def __setup_constructors(self):
        '''Set endianness and create transport-specific constructors.'''
        # Set endianness of constructors before using them.
        self._set_endian(little=True)

        self.__Length = ULInt32('Length')
        self.__Type = Enum(
                ULInt16('Type'),
                Undefined=0x0000,
                Command=0x0001,
                Data=0x0002,
                Response=0x0003,
                Event=0x0004,
                )
        # This is just a convenience constructor to get the size of a header.
        self.__Code = ULInt16('Code')
        self.__Header = Struct(
                'Header',
                self.__Length,
                self.__Type,
                self.__Code,
                self._TransactionID,
                )
        # These are the actual constructors for parsing and building.
        self.__CommandHeader = Struct(
                'CommandHeader',
                self.__Length,
                self.__Type,
                self._OperationCode,
                self._TransactionID,
                )
        self.__ResponseHeader = Struct(
                'ResponseHeader',
                self.__Length,
                self.__Type,
                self._ResponseCode,
                self._TransactionID,
                )
        self.__EventHeader = Struct(
                'EventHeader',
                self.__Length,
                self.__Type,
                self._EventCode,
                self._TransactionID,
                )
        # Apparently nobody uses the SessionID field. Even though it is
        # specified in ISO15740:2013(E), no device respects it and the session
        # number is implicit over USB.
        self.__Param = Range(0, 5, self._Parameter)
        self.__FullParam = Struct('Parameter', Array(5, self._Parameter))
        self.__FullEventParam = Struct('Parameter', Array(3, self._Parameter))
        self.__CommandTransactionBase = Struct(
                'Command',
                Embedded(self.__CommandHeader),
                Bytes('Payload',
                      lambda ctx, h=self.__Header: ctx.Length - h.sizeof()),
                )
        self.__CommandTransaction = ExprAdapter(
                self.__CommandTransactionBase,
                encoder=lambda obj, ctx, h=self.__Header: Container(
                    Length=len(obj.Payload) + h.sizeof(),
                    **obj
                    ),
                decoder=lambda obj, ctx: obj,
                )
        self.__ResponseTransactionBase = Struct(
                'Response',
                Embedded(self.__ResponseHeader),
                Bytes('Payload',
                      lambda ctx, h=self.__Header: ctx.Length - h.sizeof()),
                )
        self.__ResponseTransaction = ExprAdapter(
                self.__ResponseTransactionBase,
                encoder=lambda obj, ctx, h=self.__Header: Container(
                    Length=len(obj.Payload) + h.sizeof(),
                    **obj
                    ),
                decoder=lambda obj, ctx: obj,
                )
        self.__EventTransactionBase = Struct(
                'Event',
                Embedded(self.__EventHeader),
                Bytes('Payload',
                      lambda ctx, h=self.__Header: ctx.Length - h.sizeof()),
                )
        self.__EventTransaction = ExprAdapter(
                self.__EventTransactionBase,
                encoder=lambda obj, ctx, h=self.__Header: Container(
                    Length=len(obj.Payload) + h.sizeof(),
                    **obj
                    ),
                decoder=lambda obj, ctx: obj,
                )

    def __parse_response(self, ipdata):
        '''Helper method for parsing USB data.'''
        # Build up container with all PTP info.
        transaction = self.__ResponseTransaction.parse(ipdata)
        response = Container(
            SessionID=self.session_id,
            TransactionID=transaction.TransactionID,
        )
        if transaction.Type == 'Response':
            response['ResponseCode'] = transaction.ResponseCode
            response['Parameter'] = self.__Param.parse(transaction.Payload)
        elif transaction.Type == 'Event':
            event = self.__EventHeader.parse(
                ipdata[0:self.__Header.sizeof()]
            )
            response['EventCode'] = event.EventCode
            response['Parameter'] = self.__Param.parse(transaction.Payload)
        else:
            command = self.__CommandHeader.parse(
                ipdata[0:self.__Header.sizeof()]
            )
            response['OperationCode'] = command.OperationCode
            response['Data'] = transaction.Payload
        return response

    def __recv(self, event=False, wait=False, raw=False):
        '''Helper method for receiving non-event data.'''
        ip = self.__intip if event else self.__inip
        ipdata = ip.read(ip.wMaxPacketSize, timeout=0 if wait else 5)
        header = self.__ResponseHeader.parse(
            ipdata[0:self.__Header.sizeof()]
        )
        if header.Type not in ['Response', 'Data', 'Event']:
            raise PTPError(
                'Unexpected USB transfer type.'
                'Expected Response, Event or Data but reveived {}'
                .format(header.Type)
            )
        while len(ipdata) < header.Length:
            ipdata += ip.read(
                ip.wMaxPacketSize,
                timeout=5000
            )
        if raw:
            return ipdata
        else:
            return self.__parse_response(ipdata)

    def __send(self, ptp_container, event=False):
        '''Helper method for sending data.'''
        ip = self.__intip if event else self.__outip
        transaction = self.__CommandTransaction.build(ptp_container)
        ip.write(transaction, timeout=1)

    def __send_request(self, ptp_container):
        '''Send PTP request without checking answer.'''
        # Don't modify original container to keep abstraction barrier.
        ptp = Container(**ptp_container)
        # Don't send unused parameters
        try:
            while not ptp.Parameter[-1]:
                ptp.Parameter.pop()
                if len(ptp.Parameter) == 0:
                    break
        except IndexError:
            # The Parameter list is already empty.
            pass

        # Send request
        ptp['Type'] = 'Command'
        ptp['Payload'] = self.__Param.build(ptp.Parameter)
        self.__send(ptp)

    def __send_data(self, ptp_container, data):
        '''Send data without checking answer.'''
        # Don't modify original container to keep abstraction barrier.
        ptp = Container(**ptp_container)
        # Send data
        ptp['Type'] = 'Data'
        ptp['Payload'] = data
        self.__send(ptp)

    # Actual implementation
    # ---------------------
    def send(self, ptp_container, data):
        '''Transfer operation with dataphase from initiator to responder'''
        self.__send_request(ptp_container)
        self.__send_data(ptp_container, data)
        # Get response and sneak in implicit SessionID and missing parameters.
        return self.__recv()

    def recv(self, ptp_container):
        '''Transfer operation with dataphase from responder to initiator.'''
        self.__send_request(ptp_container)
        dataphase = self.__recv()
        if hasattr(dataphase, 'Data'):
            response = self.__recv()
            if (
                    (ptp_container.OperationCode != dataphase.OperationCode) or
                    (ptp_container.TransactionID != dataphase.TransactionID) or
                    (ptp_container.SessionID != dataphase.SessionID) or
                    (dataphase.TransactionID != response.TransactionID) or
                    (dataphase.SessionID != response.SessionID)
            ):
                raise PTPError(
                    'Dataphase does not match with requested operation.'
                )
            response['Data'] = dataphase.Data
            return response
        else:
            return dataphase

    def mesg(self, ptp_container):
        '''Transfer operation without dataphase.'''
        self.__send_request(ptp_container)
        # Get response and sneak in implicit SessionID and missing parameters
        # for FullResponse.
        return self.__recv()

    def event(self, wait=False):
        '''Check event.

        If `wait` this function is blocking. Otherwise it may return None.
        '''
        evt = None
        ipdata = None
        timeout = None if wait else 0.001
        if not self.__event_queue.empty():
            ipdata = self.__event_queue.get(block=not wait, timeout=timeout)
        if ipdata is not None:
            evt = self.__parse_response(ipdata)

        return evt
