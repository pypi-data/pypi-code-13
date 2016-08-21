from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from uuid import uuid4

__all__ = ['Uprofile']

class Uprofile(Base):
    options = {
        'code':{
            'user':{
                'access_token_auth':{
                    'nok':'81d62caaf2ba446fb85ba21489064232',
                    'ok':'fff0418d0d6f4f3bb9bb1cad6fb10e60'
                },
                'access_token_generate':{
                    'ok':'05b8d2d0d1b54c2c8621ee2857474ff5'
                },
                'not_found':'6c4ac7b57aec4e7baac90752f8d0594b'
            }
        },
        'rmq':{
            'exchange':{
                'headers':'uprofile_headers',
                'headers_any':'uprofile_headers_any',
                'topic':'uprofile'
            },
            'rk':{
                'user':{
                    'access_token_auth':'uprofile.user.access_token.auth',
                    'access_token_generate':'uprofile.user.access_token.generate',
                    'register':'uprofile.user.register'
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
        return sha1('uprofile:%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

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
        payload['etag'] = self.etag

        def on_encode(_):
            self.__channel__['pusher'].basic_publish(
                body=_.result(),
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key=rk
            )
            return True
        
        def on_response(_):
            future.set_result(_.result())
            self.__channel__['consumer'].queue_unbind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers_any'],
                arguments={
                    'etag':payload['etag'],
                    'uprofile-response':True
                }
            )
            return True

        self.__request__[payload['etag']] = self.ioengine.future(on_response)
        
        self.__channel__['consumer'].queue_bind(
            callback=None,
            queue=self.options['rmq']['queue'],
            exchange=self.options['rmq']['exchange']['headers_any'],
            arguments={
                'etag':payload['etag'],
                'uprofile-response':True
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
        
        self.rmq.channel('uprofile_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('uprofile_pusher_%s' % self.uuid,self.ioengine.future(on_pusher))
        return True

    def on_msg(self,channel,method,properties,body):
        def ack(_):
            try:
                assert _.result()
            except AssertionError:
                channel.basic_nack(method.delivery_tag)
            except:
                raise
            else:
                channel.basic_ack(method.delivery_tag)
            return True
        
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

        self.ioengine.future(ack).set_result(True)
        return True

    def user_access_token_auth(self,u,a,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_token_auth,
                    u=u,
                    a=a,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_token_auth']['ok']
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result()['body'])
                return True
            
            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'u':u,
                    'a':a
                },
                rk=self.options['rmq']['rk']['user']['access_token_auth'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def user_access_token_generate(self,email,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_token_generate,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_token_generate']['ok']
                except AssertionError:
                    def on_register(_):
                        self.ioengine.loop.add_callback(
                            self.user_access_token_generate,
                            email=email,
                            future=future
                        )
                        return True

                    self.ioengine.loop.add_callback(
                        self.user_register,
                        email=email,
                        future=self.ioengine.future(on_register)
                    )
                except:
                    raise
                else:
                    future.set_result(_.result()['body'])
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'email':email
                },
                rk=self.options['rmq']['rk']['user']['access_token_generate'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def user_register(self,email,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_register,
                    email=email
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(True)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'email':email
                },
                rk=self.options['rmq']['rk']['user']['register'],
                future=self.ioengine.future(on_response)
            )
        return True
