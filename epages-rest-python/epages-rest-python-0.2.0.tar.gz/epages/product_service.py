# coding: utf-8
'''
Author: Oliver Zscheyge
Description:
    Provides access to all the product calls provided by the epages REST API.
'''

from epages.product import Product
from epages.error import RESTError

class ProductService(object):
    """TODO
    """

    def __init__(self, client):
        """Initializer.
        Args:
            client (HTTPClient): The epages HTTP client used to make the calls.
        """
        super(ProductService, self).__init__()
        self.client = client

    def get_products(self, locale=u"", currency=u"", page=1, results_per_page=10,
                     direction=u"", sort=u"name", q=u"", category_id=u"", id=u""):
        params = {}
        products = []
        try:
            self.client.get(u"/products", params=params)
        except RESTError, error:
            print(unicode(error))
        return products

    def get_nr_products(self, locale=u"", currency=u"", page=1, results_per_page=10,
                        direction=u"", sort=u"name", q=u"", category_id=u"", id=u""):
        return -1
