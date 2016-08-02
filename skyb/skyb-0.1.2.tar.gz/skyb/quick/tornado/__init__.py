import os, os.path
import tornado.ioloop
import tornado.web


class BaseApplication(tornado.web.Application):
    def __init__(self, handlers, **kw):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        settings = dict(template_path=os.path.join(base_dir, kw.get('template_path', "./template")),
                        static_path=os.path.join(base_dir, kw.get('static_path', "./static")),
                        debug=kw.get('debug', False),
                        autoescape=None
                        )
        super(BaseApplication, self).__init__(handlers, **settings)

    def boot(self, port):
        self.listen(port)
        print 'application start at port %s' % port
        tornado.ioloop.IOLoop.instance().start()


class BaseAuthHandler(tornado.web.RequestHandler):
    def prepare(self):
        _auth = getattr(self, "_auth", None)
        if _auth is None:
            return
        auth = self.get_argument('auth', None)
        if auth is None:
            auth = self.request.headers.get("auth", None)

        if auth is None or auth != _auth:
            self.finish("auth fail")
