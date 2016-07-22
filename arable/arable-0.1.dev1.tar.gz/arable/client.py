import requests
from base64 import b64encode


class ArableClient(object):
    """A client for connecting to Arable and making data queries."""
    base_url = "https://api.arable.com/dev2"
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

    def check_connection(self):
        """Returns True if client has auth token, raises an exception if not"""
        if not self.token:
            raise Exception("Authentication exception: not connected.")
        return True

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
            raise Exception("Failed to connect:\n{}".format(e.message))

    def deployments(self, device_id=None, deployment_id=None):
        """ Lists the current deployments associated with the user's group.

            :param device_id : optional; list all deployments for the specified
            device; ignored if deployment_id is present
            :param deployment_id : optional; list the specified deployment;
            takes precedence over device_id, if present
        """

        self.check_connection()

        if deployment_id:
            url = ArableClient.base_url + "/deployments/" + deployment_id
        elif device_id:
            url = "{0}/devices/{1}/deployments".format(
                ArableClient.base_url, device_id)
        else:
            url = ArableClient.base_url + "/deployments"
        headers = {"Authorization": self.token}

        r = requests.get(url, headers=headers)
        if 200 == r.status_code:
            return r.json()
        else:
            r.raise_for_status()

    def devices(self, device_id=None, name=None):
        """ Lists the devices associated with the user's group.

            :param device_id : optional; look up a single device by id; takes
            precedence over name, if present
            :param name : optional; look up a single device by name (serial);
            ignored if device_id is present
        """

        self.check_connection()

        url = ArableClient.base_url + "/devices"
        if device_id:
            url += "/" + device_id
        elif name:
            url += "?name=" + name
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

        self.check_connection()

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
