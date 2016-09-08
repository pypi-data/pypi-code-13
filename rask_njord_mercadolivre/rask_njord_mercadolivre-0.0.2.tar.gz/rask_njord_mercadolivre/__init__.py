from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import ack,BasicProperties
from uuid import uuid4

__all__ = ['Meli']

class Meli(Base):
    options = {
        'code':{
            'auth':{
                'tuid':{
                    'ok':'1dafcbd0b36a4f64b9a98ff29c248db4'
                }
            }
        },
        'rmq':{
            'exchange':{
                'headers':'mercadolivre_headers',
                'topic':'mercadolivre'
            },
            'rk':{
                'auth':{
                    'tuid':'mercadolivre.auth.tuid'
                }
            }
        }
    }
    
    def __init__(self,rmq):
        self.options['rmq']['queue'] = self.etag
        self.rmq = rmq
        self.utcode = UTCode()
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
        except (AssertionError,AttributeError):
            self.__active = False
        except:
            raise
        return self.__active
    
    @active.setter
    def active(self,_):
        try:
            assert _
            assert 'consumer' in self.__channel__
            assert 'pusher' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)
        
    @property
    def etag(self):
        return sha1('meli:%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

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

    def __push__(self,payload,rk,future):
        etag = self.etag

        def on_encode(_):
            self.__channel__['pusher'].basic_publish(
                body=_.result(),
                exchange=self.options['rmq']['exchange']['topic'],
                properties=BasicProperties(headers={'etag':etag}),
                routing_key=rk
            )
            return True
        
        def on_response(_):
            future.set_result(_.result())
            self.__channel__['consumer'].queue_unbind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers'],
                arguments={
                    'etag':etag,
                    'meli-response':True,
                    'x-match':'all'
                }
            )
            return True

        self.__request__[etag] = self.ioengine.future(on_response)
        
        self.__channel__['consumer'].queue_bind(
            callback=None,
            queue=self.options['rmq']['queue'],
            exchange=self.options['rmq']['exchange']['headers'],
            arguments={
                'etag':etag,
                'meli-response':True,
                'x-match':'all'
            }
        )

        self.utcode.encode(payload,future=self.ioengine.future(on_encode))
        return True
    
    def __services__(self):
        def on_consumer(_):
            self.log.info('channel consumer')
            self.__channel__['consumer'] = _.result().channel
            self.ioengine.loop.add_callback(self.__queue_declare__)
            return True
        
        def on_pusher(_):
            self.log.info('channel pusher')
            self.__channel__['pusher'] = _.result().channel
            return True
        
        self.rmq.channel('meli_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('meli_pusher_%s' % self.uuid,self.ioengine.future(on_pusher))
        return True  

    def auth_tuid(self,uid,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.auth_tuid,
                    uid=uid,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['auth']['tuid']['ok']
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result()['body'])
                return True
            
            self.ioengine.loop.add_callback(
                self.__push__,
                payload=uid,
                rk=self.options['rmq']['rk']['auth']['tuid'],
                future=self.ioengine.future(on_response)
            )
            
            self.log.info('creating tuid')
        return True
    
    def on_msg(self,channel,method,properties,body):
        try:
            assert properties.headers['etag'] in self.__request__
        except AssertionError:
            channel.basic_publish(
                body=body,
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key='',
                properties=properties
            )
        except KeyError:
            pass
        except:
            raise
        else:
            def on_decode(_):
                self.__request__[properties.headers['etag']].set_result({'header':properties.headers,'body':_.result()})
                del self.__request__[properties.headers['etag']]
                return True

            self.utcode.decode(body,future=self.ioengine.future(on_decode))

        ack(channel,method)(True)
        return True
