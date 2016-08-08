from rask.http import WSHandler
from rask.options import options
from rask.parser.date import datetime2timestamp
from rask.parser.utcode import UTCode
import udatetime

__all__ = ['DefaultHandler']

class DefaultHandler(WSHandler):
    def call(self,msg):
        try:
            assert msg['header']['action'] in self.actions
        except AssertionError:
            self.error(
                options.redefiscal_ws['code']['ws']['ns']['invalid'],
                msg['header']['etag']
            )
        except:
            raise
        else:
            self.ioengine.loop.add_callback(
                self.actions[msg['header']['action']],
                msg=msg,
                io=self
            )
        return True

    def error(self,code,etag=None):
        self.push({
            "header":{
                "action":"error",
                "code":code,
                "etag":etag
            }
        })
        return True
    
    def on_message(self,msg):
        def on_decode(_):
            try:
                assert _.result()['header']['etag']
            except (AssertionError,AttributeError,KeyError):
                self.error(options.redefiscal_ws['code']['ws']['payload']['invalid'])
            except:
                raise
            else:
                self.ioengine.loop.add_callback(
                    self.call,
                    msg=_.result()
                )
            return True
        
        self.utcode.decode(msg,future=self.ioengine.future(on_decode))
        return True
    
    def open(self):
        self.actions = options.redefiscal_ws['actions']
        self.skernel = options.redefiscal_ws['skernel']
        self.utcode = UTCode()

        self.log.info('connected: %s [%s]' % (self.request.remote_ip,self.uuid))        
        self.set_nodelay(True)
        self.skernel.connection_add(self)
        self.push({"header":{"action":"raid.welcome","method":"who"}})
        return True

    def on_close(self):
        self.log.info('closed: %s [%s]' % (self.request.remote_ip,self.uuid))
        self.skernel.connection_del(self.uuid)
        return True

    def push(self,_):
        def on_encode(payload):
            self.write_message(payload.result())
            return True

        _['header']['__sysdate__'] = datetime2timestamp(udatetime.utcnow())
        self.utcode.encode(_,future=self.ioengine.future(on_encode))
        return True
