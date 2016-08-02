from rask.base import Base
from tornado.web import asynchronous,RequestHandler

__all__ = ['Handler']

class Handler(RequestHandler,Base):
    def set_default_headers(self):
        self.set_header('Server','Viking Makt HTTP Server')

