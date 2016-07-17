from hashlib import sha1
from .msg import KDelPayload,KGetPayload,KGetResponse,KSetPayload
from rask.base import Base
from rask.parser.pb import decode,encode
from rask.rmq import BasicProperties
from uuid import uuid4

__all__ = ['Riak']

class Riak(Base):
    options = {
        'rmq':{
            'exchange':{
                'headers':'njord_riak_headers_all',
                'headers_any':'njord_riak_headers_any',
                'topic':'njord_riak'
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
        except (AttributeError,AssertionError):
            self.__active = False
        except:
            raise
        return self.__active
    
    @active.setter
    def active(self,_):
        try:
            assert _
            assert 'consumer' in self.__channel__
            assert 'delete' in self.__channel__
            assert 'get' in self.__channel__
            assert 'store' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)
            
    @property
    def etag(self):
        return sha1('%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

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
        
        def on_delete(_):
            self.log.info('channel del')
            self.__channel__['delete'] = _.result().channel
            self.active = True
            return True
        
        def on_get(_):
            self.log.info('channel get')
            self.__channel__['get'] = _.result().channel
            self.active = True
            return True

        def on_store(_):
            self.log.info('channel store')
            self.__channel__['store'] = _.result().channel
            self.active = True
            return True

        self.rmq.channel('riak_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('riak_delete_%s' % self.uuid,self.ioengine.future(on_delete))
        self.rmq.channel('riak_get_%s' % self.uuid,self.ioengine.future(on_get))
        self.rmq.channel('riak_store_%s' % self.uuid,self.ioengine.future(on_store))
        return True

    def delete(self,cluster,bucket,key):
        try:
            assert self.active
        except AssertionError:
            def callback(_):
                self.ioengine.loop.add_callback(
                    self.delete,
                    cluster=cluster,
                    bucket=bucket,
                    key=key
                )
                return True
            
            self.promises.append(self.ioengine.future(callback))
            return None
        except:
            raise
        else:
            self.__channel__['delete'].basic_publish(
                body=encode(KDelPayload(
                    cluster=cluster,
                    bucket=bucket,
                    key=key
                )),
                exchange='',
                properties=BasicProperties(headers={
                    'cluster':cluster,
                    'service':'del'
                }),
                routing_key=''
            )
        return True
    
    def get(self,cluster,bucket,key,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.get,
                    cluster=cluster,
                    bucket=bucket,
                    key=key,
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
                future.set_result(decode(_.result(),KGetResponse()))
                self.__channel__['consumer'].queue_unbind(
                    callback=None,
                    queue=self.options['rmq']['queue'],
                    exchange=self.options['rmq']['exchange']['headers_any'],
                    arguments={
                        'etag':etag
                    }
                )
                return True
            
            self.__channel__['consumer'].queue_bind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers_any'],
                arguments={
                    'etag':etag
                }
            )

            self.__request__[etag] = self.ioengine.future(on_response)
            self.__channel__['get'].basic_publish(
                body=encode(KGetPayload(
                    cluster=cluster,
                    bucket=bucket,
                    key=key,
                    etag=etag
                )),
                exchange=self.options['rmq']['exchange']['topic'],
                properties=BasicProperties(headers={
                    'cluster':cluster,
                    'service':'kget'
                }),
                routing_key=''
            )
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
        except AssertionError:
            pass
        except KeyError:
            self.ioengine.future(ack).set_result(True)
        except:
            raise
        else:
            self.__request__[properties.headers['etag']].set_result(body)
            self.ioengine.future(ack).set_result(True)
            del self.__request__[properties.headers['etag']]
        return True
    
    def store(self,cluster,bucket,key,data,content_type='application/json'):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.store,
                    cluster=cluster,
                    bucket=bucket,
                    key=key,
                    data=data,
                    content_type=content_type
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
            return None
        except:
            raise
        else:        
            self.__channel__['store'].basic_publish(
                body=encode(KSetPayload(
                    cluster=cluster,
                    bucket=bucket,
                    key=key,
                    data=data,
                    content_type=content_type,
                    etag=self.etag
                )),
                exchange=self.options['rmq']['exchange']['topic'],
                properties=BasicProperties(headers={
                    'cluster':cluster,
                    'service':'kset'
                }),
                routing_key=''
            )
        return True
