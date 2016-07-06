class BaseService(object):

    def __init__(self,
            base_url=None,
            post_method=None,
            api_key=None,
            verify=True,
            timeout=None):
        """
        """
        self.base_url = base_url
        self.api_key = api_key


    def query(self, method, *args, **kwargs):
        """
        """
        url = self.base_url + '/' + method

        data = self._format_data(*args, **kwargs)

        response = self._post(url, data)

        return self._parse_response(response)


    def _format_data(self, method, *args, **kwargs):
        if args and kwargs:
            raise ValueError('Mixing of keyword arguments and positional arguments '
                             'when querying predictive service is not supported.')

        return json.dumps(args or kwargs)


    def _post(self, url, data)
        if not self.session:
            import requests
            self.session = requests.session()

        response = self.session.post(
                url=url,
                data=data,
                headers=headers,
                verify=verify,
                timeout=timeout,
                auth=HTTPBasicAuth('api_key', api_key))



    def _parse_response(self, response):
        return json.loads(response)

