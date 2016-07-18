from tapioca import (TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)
from requests_oauthlib import OAuth2
from .sently_resource_mapping import RESOURCE_MAPPING
from helpers import sentlyinfo

class SentlyClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://apiserver.sent.ly/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(SentlyClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['auth'] = OAuth2(
            api_params.get('client_id', ''), token={
                'access_token': api_params.get('access_token'),
                'token_type': 'Bearer'})
        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass

Sently = generate_wrapper_from_adapter(SentlyClientAdapter)
Sently.info = sentlyinfo
