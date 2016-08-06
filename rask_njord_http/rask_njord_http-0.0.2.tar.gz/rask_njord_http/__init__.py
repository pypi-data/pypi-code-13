from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import BasicProperties
from uuid import uuid4

__all__ = ['HTTP']

class HTTP(Base):
    options = {
        'rmq':{
            'exchange':{
                'headers':'njord_http_headers',
                'headers_any':'njord_http_headers_any',
                'topic':'njord_http'
            },
            'rk':{
                'fetch':'njord.http.request'
            }
        }
    }
    
    def __init__(self,rmq):
        self.options['rmq']['queue'] = self.etag
        self.rmq = rmq
        self.ioengine.loop.add_callback(self.__services__)

    @property
    def __channel__(self):
        try:
            assert self.__channel
        except (AssertionError,AttributeError):
            self.__channel = {}
        except:
            raise
        return self.__channel

    @property
    def __request__(self):
        try:
            assert self.__request
        except (AssertionError,AttributeError):
            self.__request = {}
        except:
            raise
        return self.__request
    
    @property
    def active(self):
        try:
            assert self.__active
        except (AssertionError,AttributeError,):
            self.__active = False
        except:
            raise
        return self.__active

    @active.setter
    def active(self,_):
        try:
            assert _
            assert 'consumer' in self.__channel__
            assert 'fetch' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)
        
    @property
    def etag(self):
        return sha1('njord-http[%s:%s]' % (self.uuid,uuid4().hex)).hexdigest()

    @property
    def utcode(self):
        try:
            assert self.__utcode
        except (AssertionError,AttributeError):
            self.__utcode = UTCode()
        except:
            raise
        return self.__utcode
    
    def __queue_declare__(self):
        def on_declare(*args):
            self.__channel__['consumer'].basic_consume(
                consumer_callback=self.on_msg,
                queue=self.options['rmq']['queue']
            )
            self.active = True
            return True
        
        self.__channel__['consumer'].queue_declare(
            callback=on_declare,
            queue=self.options['rmq']['queue'],
            durable=False,
            exclusive=True
        )
        return True
    
    def __services__(self):
        def on_consumer(_):
            self.log.info('channel consumer')
            self.__channel__['consumer'] = _.result().channel
            self.ioengine.loop.add_callback(self.__queue_declare__)
            return True
        
        def on_fetch(_):
            self.log.info('channel fetch')
            self.__channel__['fetch'] = _.result().channel
            return True

        self.rmq.channel('http_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('http_fetch_%s' % self.uuid,self.ioengine.future(on_fetch))
        return True

    def fetch(self,request,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.fetch,
                    request=request,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
            return None
        except:
            raise
        else:
            etag = self.etag
           
            def on_response(_):
                def on_decode(msg):  
                    future.set_result(msg.result())
                    self.__channel__['consumer'].queue_unbind(
                        callback=None,
                        queue=self.options['rmq']['queue'],
                        exchange=self.options['rmq']['exchange']['headers_any'],
                        arguments={'etag':etag}
                    )
                    return True

                self.utcode.decode(_.result(),future=self.ioengine.future(on_decode))
                return True

            def on_encode(_):
                self.__channel__['fetch'].basic_publish(
                    body=_.result(),
                    exchange=self.options['rmq']['exchange']['topic'],
                    properties=BasicProperties(headers={
                        'etag':etag,
                        'service':'fetch'
                    }),
                    routing_key=self.options['rmq']['rk']['fetch']
                )
                return True
                
            self.__channel__['consumer'].queue_bind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers_any'],
                arguments={
                    'njord-http-response':True,
                    'etag':etag
                }
            )

            self.__request__[etag] = self.ioengine.future(on_response)
            self.utcode.encode(request,self.ioengine.future(on_encode))
        return True
    
    def on_msg(self,channel,method,properties,body):
        def ack(_):
            try:
                assert _
            except AssertionError:
                channel.basic_nack(method.delivery_tag)
                self.log.debug('nack %s' % method.delivery_tag)
            except:
                raise
            else:
                channel.basic_ack(method.delivery_tag)
                self.log.debug('ack %s' % method.delivery_tag)
            return True

        try:
            assert properties.headers['etag'] in self.__request__
        except (AssertionError,KeyError):
            self.ioengine.future(ack).set_result(True)
        except:
            raise
        else:
            self.__request__[properties.headers['etag']].set_result(body)
            self.ioengine.future(ack).set_result(True)
            del self.__request__[properties.headers['etag']]
        return True
