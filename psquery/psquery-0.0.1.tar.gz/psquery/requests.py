from .base import Base

import requests

class RequestsMixin(Base):

    def __init__(self, base_url, api_key, verify):
        Base.__init__(self, base_url=base_url, api_key=api_key)
        self.verify = verify

