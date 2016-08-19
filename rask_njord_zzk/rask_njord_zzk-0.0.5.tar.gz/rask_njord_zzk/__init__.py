from rask.base import Base

__all__ = ['ZZK']

class ZZK(Base):
    options = {
        'url':'http://api.00k.srv.br'
    }
    
    def __init__(self,token,http):
        self.http = http
        self.token = token

    @property
    def request(self):
        return {'headers':{'Authorization':self.token,'Content-Type':'application/json;charset=UTF-8'},'request_timeout':60.0}

    def get_category(self,uid,future):
        def on_fetch(_):
            future.set_result(_.result())
            return True
        
        request = self.request
        request['method'] = 'GET'
        request['url'] = '%s/catalog/categories?externalid=%s' % (self.options['url'],uid)
        
        self.http.fetch(request,future=self.ioengine.future(on_fetch))
        return True
    
    def get_sku(self,sku,future):
        def on_fetch(_):
            future.set_result(_.result())
            return True
        
        request = self.request
        request['method'] = 'GET',
        request['url'] = '%s/catalog/products/all?sku=%s' % (self.options['url'],sku)
        
        self.http.fetch(request,future=self.ioengine.future(on_fetch))
        return True
