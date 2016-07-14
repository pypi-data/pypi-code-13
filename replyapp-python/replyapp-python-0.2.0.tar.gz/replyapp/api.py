import requests
import re
import json

class ReplyAppError(Exception):
    def __init__(self, response):
        self.response = response

class ReplyApp():
    '''
    ReplyApp
    A python 3 wrapper for v1 of the ReplyApp api
    This wrapper uses getattr to build complete urls.
    Use dot notation to complete the URLS.
    You can use 3 different parameters to construct the url:
        data: Data which is passed within the body of the request
        params: Data which is passed as parameters (?email=testing@blitzen.com) etc.
        method: POST, GET, PUT, DELETE. If method is omitted, it defaults to GET
    '''
    def __init__(self, api_key, *args, **kwargs):
        self.api_key = api_key
        self.api_version = 'v1'
        self.base_url = 'https://run.replyapp.io/api/' + self.api_version + '/'
        self._attr_path = []
        self._request_method = {
            'POST': requests.post,
            'GET': requests.get,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

    def __call__(self, *args, **kwargs):
        '''
        Call will create the url based off all attrs passed after the ReplyApp object
        It will also take in data (Body data), params (Query parameters) and method
        '''
        url = self.base_url + '/'.join(self._attr_path)
        for variable_name, variable_sub in kwargs.get('variable', {}).items():
            url = re.sub(variable_name, variable_sub, url)
        self._attr_path = []
        return self._request(url,
                            kwargs.get('data', {}),
                            kwargs.get('method', 'GET'),
                            kwargs.get('params', {}))

    def __getattr__(self, attr, *args, **kwargs):
        '''
        Overwrite the getattr function in python to add each element form the dot notation
        to the _attr_path.
        The _attr_path is then used within __call__ to make the entire request
        '''
        self._attr_path.append(attr)
        return self

    def _request(self, endpoint, data, method='GET', params = None):
        '''
        _request will actually make the request, and return the response json if the code is
        successful.
        This function will return the json from the response
        If an error occurs, it will raise a requests raise_for_status exception
        '''
        headers = {'Content-Type': 'application/json'}
        params['apiKey'] = self.api_key
        if type(data) == dict:
            data = json.dumps(data)
        try:
            request = self._request_method[method]
        except KeyError as e:
            raise ReplyAppError(e.value)
        response = request(endpoint,
                           data=data,
                           params=params,
                           headers=headers)
        if response.status_code < 400:
            if response.text != '':
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()
