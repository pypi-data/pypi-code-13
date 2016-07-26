import chargehound
import requests_mock
import unittest2
import json

from chargehound.version import VERSION


get_headers = {
    'accept': 'application/json',
    'authorization': 'Basic QVBJX0tFWTo=',
    'user-agent': 'Chargehound/v1 PythonBindings/' + VERSION
}

post_headers = {
    'accept': 'application/json',
    'authorization': 'Basic QVBJX0tFWTo=',
    'content-type': 'application/json',
    'user-agent': 'Chargehound/v1 PythonBindings/' + VERSION
}

product_info = [{'name': 'Saxophone',
                 'description': 'Alto saxophone, with carrying case',
                 'image': 'http://s3.amazonaws.com/chargehound/saxophone.png',
                 'sku': '17283001272',
                 'quantity': 1,
                 'amount': 20000,
                 'url': 'http://www.example.com', },
                {'name': 'Milk',
                 'description': 'Semi-skimmed Organic',
                 'image': 'http://s3.amazonaws.com/chargehound/milk.png',
                 'sku': '26377382910',
                 'quantity': '64oz',
                 'amount': 400,
                 'url': 'http://www.example.com'}]


def is_json(response_body):
    """Can this HTTP response be parsed as JSON?"""
    try:
        json.loads(response_body)
        return True
    except:
        return False


def json_has_structure(response_body, expected_json):
    """Does the JSON this HTTP response match the expected structure?"""
    actual_json = json.loads(response_body)

    return actual_json == expected_json


class DisputeTest(unittest2.TestCase):

    def setUp(self):
        super(DisputeTest, self).setUp()
        chargehound.api_key = 'API_KEY'

    @requests_mock.mock()
    def test_retrieve_dispute(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes/dp_123',
                 status_code=200,
                 request_headers=get_headers,
                 json={'id': 'dp_123'})
        chargehound.Disputes.retrieve('dp_123')
        assert mock.called

    @requests_mock.mock()
    def test_list_all_disputes(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes',
                 status_code=200,
                 request_headers=get_headers,
                 json={'data': [{'id': 'dp_123'}]})
        chargehound.Disputes.list()
        assert mock.called

    @requests_mock.mock()
    def test_submit_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json={'id': 'dp_123'})
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'})

        assert mock.called

        response = mock.request_history[0].body

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'}})

    @requests_mock.mock()
    def test_submit_dispute_with_product_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json={'id': 'dp_123'})
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    products=product_info)

        assert mock.called

        response = mock.request_history[0].body

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'products': product_info})

    @requests_mock.mock()
    def test_update_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123',
                  status_code=200,
                  json={'id': 'dp_123'})
        chargehound.Disputes.update('dp_123',
                                    fields={'customer_name': 'Susie'})

        assert mock.called

        response = mock.request_history[0].body

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'}})

    @requests_mock.mock()
    def test_update_dispute_with_product_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123',
                  status_code=200,
                  json={'id': 'dp_123'})
        chargehound.Disputes.update('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    products=product_info)

        assert mock.called

        response = mock.request_history[0].body

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'products': product_info})
