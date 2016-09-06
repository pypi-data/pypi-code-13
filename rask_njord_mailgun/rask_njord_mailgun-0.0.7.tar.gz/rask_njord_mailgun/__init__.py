from hashlib import sha1
from rask.base import Base
from rask.parser.json import dictfy
from rask.parser.utcode import UTCode
from rask.rmq import ack
from uuid import uuid4

__all__ = ['Mailgun']

class Mailgun(Base):
    options = {
        'rmq':{
            'exchange':{
                'headers':'njord_mailgun_headers',
                'headers_any':'njord_mailgun_headers_any',
                'topic':'njord_mailgun'
            },
            'rk':{
                'mail.send':'njord_mailgun.mail.send',
                'mail.validate':'njord_mailgun.mail.validate'
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
        return sha1('mailgun:%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

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
                    'njord-mailgun-response':True
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
                'njord-mailgun-response':True
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
        
        self.rmq.channel('mailgun_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('mailgun_pusher_%s' % self.uuid,self.ioengine.future(on_pusher))
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
            self.utcode.decode(body,future=self.__request__[properties.headers['etag']])
            del self.__request__[properties.headers['etag']]

        ack(channel,method).set_result(True)
        return True
    
    def mail_send(self,apikey,domain,mail,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.mail_send,
                    apikey=apikey,
                    domain=domain,
                    mail=mail,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['code'] == 200
                except (AssertionError,KeyError):
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(dictfy(_.result()['body']))
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'apikey':apikey,
                    'domain':domain,
                    'mail':mail
                },
                rk=self.options['rmq']['rk']['mail.send'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def mail_validate(self,apikey,address,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.mail_validate,
                    apikey=apikey,
                    address=address,
                    future=future
                )
                return True
            
            self.promises.append(self.ioengine.future(on_active))
            return None
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['code'] == 200
                    body = dictfy(_.result()['body'])
                    assert body['is_valid']
                except (AssertionError,KeyError):
                    future.set_result(False)
                    self.log.info('mail validate: %s 0' % address)
                except:
                    raise
                else:
                    future.set_result(dictfy(_.result()['body']))
                    self.log.info('mail validate: %s 1' % address)
                return True
            
            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'apikey':apikey,
                    'address':address
                },
                rk=self.options['rmq']['rk']['mail.validate'],
                future=self.ioengine.future(on_response)
            )

            self.log.info('mail validate: %s' % address)
        return True
