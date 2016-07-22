import requests
from base64 import b64encode


class ArableClient(object):
    """A client for connecting to Arable and making data queries."""
    base_url = "https://cuyk6i17yd.execute-api.us-east-1.amazonaws.com/dev2"
    param_options = {"devices", "deployments", "start", "end", "order",
                     "limit", "format", "select"}

    def __init__(self):
        self.token = None

    def _login(self, email, password, group_id):
        url = "{0}/auth/user/{1}".format(ArableClient.base_url, group_id)
        token = b64encode("{0}:{1}".format(email, password))
        headers = {"Authorization": "Basic " + token}

        r = requests.post(url, headers=headers)
        if r.status_code == 200:
            return "Bearer " + r.json()['access_token']
        else:
            r.raise_for_status()

    def connect(self, email=None, password=None, group_id=None):
        """Logs the client in to the API.

            :param email : user email address
            :param password : user password
            :param group_id : user's group ID (a UUID string)
        """
        if not all([email, password, group_id]):
            raise Exception("Missing parameter; connect requires email, password, and group id")    # NOQA
        try:
            self.token = self._login(email, password, group_id)
        except Exception as e:
            print "Failed to connect:\n", e.message

    def devices(self):
        """lists the devices associated with the user's group"""

        if not self.token:
            raise Exception("Authentication exception.")

        url = ArableClient.base_url + "/devices"
        headers = {"Authorization": self.token}
        r = requests.get(url, headers=headers)
        if 200 == r.status_code:
            return r.json()
        else:
            r.raise_for_status()

    def query(self, **kwargs):
        """Query Arable pod data.

            :param devices : optional; list of devices to retrieve data for;
            ignored if deployments are specified
            :param deployments : optional; list of deployments to retrieve data
            for; devices list is ignored if this parameter is provided
            :param start : optional; beginning of query time range
            :param end : optional; end of query time range
            :param order : optional; "time" (time ascending) or "-time" (time
            descending)
            :param limit : optional; maximum number of data points to return;
            defaults to 1000
            :param format : optional; use format=csv to get csv-formatted data;
            otherwise data is returned as json
            :param select : optional; "all", "spectrometer", or "microclimate"
        """
        if not self.token:
            raise Exception("You must connect before querying.")

        url = ArableClient.base_url + "/data"
        headers = {"Authorization": self.token}
        params = {}
        for param in ArableClient.param_options:
            if kwargs.get(param):
                params[param] = str(kwargs[param])
        if not params.get('order'):
            params['order'] = '-time'
        if not params.get('limit'):
            params['limit'] = '1000'

        r = requests.get(url, headers=headers, params=params)

        if r.status_code == 200:
            if params.get('format') == 'csv':
                return r.text
            else:
                return r.json()
        else:
            r.raise_for_status()
