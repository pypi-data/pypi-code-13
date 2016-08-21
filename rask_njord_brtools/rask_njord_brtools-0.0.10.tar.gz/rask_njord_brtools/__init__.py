from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import BasicProperties
from uuid import uuid4

__all__ = ['BRTools']

class BRTools(Base):
    options = {
        'rmq':{
            'exchange':{
                'cpf':{
                    'h':'cpf_headers',
                    't':'cpf'
                }
            },
            'rk':{
                'cpf':{
                    'get':'cpf.get',
                    'validator':'cpf.validator'
                }
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
            assert 'push' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)
        
    @property
    def etag(self):
        return sha1('njord-brtools[%s:%s]' % (self.uuid,uuid4().hex)).hexdigest()

    @property
    def utcode(self):
        try:
            assert self.__utcode
        except (AssertionError,AttributeError):
            self.__utcode = UTCode()
        except:
            raise
        return self.__utcode

    def __consumer_register__(self,_=None):
        try:
            ex = _.next()
        except AttributeError:
            self.ioengine.loop.add_callback(
                self.__consumer_register__,
                _=iter(self.options['rmq']['exchange'])
            )
            return None
        except StopIteration:
            self.active = True
            return True
        except:
            raise
        else:
            def next_bind(*args):
                self.ioengine.loop.add_callback(
                    self.__consumer_register__,
                    _=_
                )
                return True

            self.__channel__['consumer'].queue_bind(
                callback=next_bind,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange'][ex]['h'],
                arguments={
                    'brtools-consumer':self.options['rmq']['queue'],
                    'brtools-response':True,
                    'x-match':'all'
                }
            )
        return None
    
    def __queue_declare__(self):
        def on_declare(*args):
            self.__channel__['consumer'].basic_consume(
                consumer_callback=self.on_msg,
                queue=self.options['rmq']['queue']
            )
            self.ioengine.loop.add_callback(self.__consumer_register__)
            return True
        
        self.__channel__['consumer'].queue_declare(
            callback=on_declare,
            queue=self.options['rmq']['queue'],
            durable=False,
            exclusive=True
        )
        return True

    def __push__(self,payload,rk,ex,future):
        etag = self.etag

        def on_encode(_):
            self.__channel__['push'].basic_publish(
                body=_.result(),
                exchange=ex,
                properties=BasicProperties(headers={
                    'brtools-consumer':self.options['rmq']['queue'],
                    'etag':etag
                }),
                routing_key=rk
            )
            return True
        
        def on_response(_):
            future.set_result(_.result())
            return True

        self.__request__[etag] = self.ioengine.future(on_response)
        self.utcode.encode(payload,future=self.ioengine.future(on_encode))
        return True
    
    def __services__(self):
        def on_consumer(_):
            self.log.info('channel consumer')
            self.__channel__['consumer'] = _.result().channel
            self.ioengine.loop.add_callback(self.__queue_declare__)
            return True
        
        def on_push(_):
            self.log.info('channel push')
            self.__channel__['push'] = _.result().channel
            return True

        self.rmq.channel('brtools_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('brtools_push_%s' % self.uuid,self.ioengine.future(on_push))
        return True

    def cpf_get(self,cpf,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.cpf_get,
                    cpf=cpf,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=str(cpf),
                ex=self.options['rmq']['exchange']['cpf']['t'],
                rk=self.options['rmq']['rk']['cpf']['get'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def cpf_validator(self,cpf,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.cpf_validator,
                    cpf=cpf,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=str(cpf),
                ex=self.options['rmq']['exchange']['cpf']['t'],
                rk=self.options['rmq']['rk']['cpf']['validator'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def on_msg(self,channel,method,properties,body):
        def ack(_):
            try:
                assert _
            except AssertionError:
                channel.basic_nack(method.delivery_tag)
                self.log.info('nack %s' % method.delivery_tag)
            except:
                raise
            else:
                channel.basic_ack(method.delivery_tag)
                self.log.info('ack %s' % method.delivery_tag)
            return True

        try:
            assert properties.headers['etag'] in self.__request__
        except (AssertionError,KeyError):
            pass
        except:
            raise
        else:
            self.utcode.decode(body,future=self.__request__[properties.headers['etag']])
            del self.__request__[properties.headers['etag']]
            
        self.ioengine.future(ack).set_result(True)
        return True
