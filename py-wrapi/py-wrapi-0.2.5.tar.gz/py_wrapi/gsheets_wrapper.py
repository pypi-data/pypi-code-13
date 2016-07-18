from tapioca import (TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)
from requests_oauthlib import OAuth2
from .gsheets_resource_mapping import RESOURCE_MAPPING
from helpers import gsheetsinfo, google_auth

access_token = None

class GSheetsClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://sheets.googleapis.com/v4/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(GSheetsClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['auth'] = OAuth2(
            api_params.get('client_id', ''), token={
                'access_token': self.auth(api_params.get('client_id'), api_params.get('client_secret')),
                'token_type': 'Bearer'})
        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass

    def auth(self, client_id, client_secret):
        global access_token
        if not access_token:
            scope = 'https://www.googleapis.com/auth/spreadsheets'
            access_token = google_auth(client_id, client_secret, scope)
        return access_token

GSheets = generate_wrapper_from_adapter(GSheetsClientAdapter)
GSheets.info = gsheetsinfo
