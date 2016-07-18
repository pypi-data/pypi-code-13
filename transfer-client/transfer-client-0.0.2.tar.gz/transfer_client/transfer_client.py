import json
import requests


class TransferClient(object):
    def __init__(self, server_name):
        """
        Initialise the class.

        :arg str server_name: Name or IP of the transfer server.
        """
        self.server_name = server_name
        self._verify = False

    def _request(self, method, endpoint, headers=None, files=None, json=None):
        """
        Handle a request.

        :arg str method: Method for the request.
        :arg str endpoint: API endpoint.
        :arg dict headers: Dictionary of HTTP Headers to send with the request.
        :arg dict files: Dictionary of file like objects for multipart encoding
            upload.
        :arg dict json: JSON data to send in the body of the request.

        :returns dict: JSON encoded content of the response.
        """
        response = requests.request(method,
            'https://{}/{}'.format(self.server_name, endpoint),
            headers=headers, files=files, json=json, verify=self._verify)
        if not response.ok:
            raise ValueError(response.json()['error'])
        return response.json()

    def users(self, user_id):
        """
        Gives a JSON object of a user together with its transfers.

        :arg str user_id: User ID.

        :returns dict: A JSON object of a user together with its transfers.
        """
        return self._request('get', 'users', {'User-Id': user_id})

    def schema(self, user_id):
        """
        Gives the JSON schema for a user.

        :arg str user_id: User ID.

        :returns dict: JSON schema.
        """
        return self._request('get', 'users/schema', {'User-Id': user_id})

    def transfers(self, user_id, metadata):
        """
        Initiates a new transfer.

        :arg str user_id: User ID.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'post', 'transfers', {'User-Id': user_id},
            {'metadata': json.dumps(metadata)})

    def status(self, user_id, transfer_id):
        """
        Gives a JSON object of a transfer.

        :arg str user_id: User ID.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'get', 'transfers/{}'.format(transfer_id), {'User-Id': user_id})

    def update(self, user_id, transfer_id, status):
        """
        Updates a transfer.

        :arg str user_id: User ID.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'put', 'transfers/{}'.format(transfer_id), {'User-Id': user_id},
            json={'status': status})

    def uploads(self, user_id, transfer_id, file_handle):
        """
        Uploads a file to a transfer.

        :arg str user_id: User ID.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'post', 'transfers/{}/uploads'.format(transfer_id),
            {'User-Id': user_id}, {'upload': file_handle})

    def completed(self, client_id):
        """
        Gives a JSON object of all transfers for this client, i.e., a list of
        transfer ids.

        :arg str client_id: Client ID.

        :returns dict: JSON object of all transfers.
        """
        return self._request('get', 'completed', {'Client-Id': client_id})
