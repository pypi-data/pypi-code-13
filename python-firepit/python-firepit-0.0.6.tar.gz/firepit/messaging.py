import json

import requests

from firepit.exception import FirebaseException


class FirebaseClient:
    _http_google_message_api = 'https://fcm.googleapis.com/fcm/send'
    _http_google_notification_api = \
        'https://android.googleapis.com/gcm/notification'

    _notification_required_fields = ('body', 'title',)
    _notification_allowed_fields = ['icon'].append(
        _notification_required_fields)

    ALLOWED_PROTOCOLS = ('http',)  # later we will support xmpp

    def __init__(self, auth_key, protocol='http', sender_id=None):
        if not auth_key:
            raise ValueError('No auth_key specified. This is required for '
                             'calls against the Google-api.')
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise ValueError('No protocol defined or not compatible.'
                             'Please use only allowed protocols ({})'
                             .format(self.ALLOWED_PROTOCOLS))
        self.auth_key = auth_key
        self.sender_id = sender_id
        self.headers = {'Authorization': 'key={}'.format(self.auth_key)}

    def send_message(self, to, priority='normal', ttl=None,
                     data=None, notification=None):
        """
        Sends a message to one or more devices or groups using
        the notification_keys.
        :param to: notification_key of one or more devices/groups
        :param priority: normal or high
        :param ttl: time to life in seconds
        :param data: your data-payload as dict
        :param notification: notification to display related to your app
        :return: data as dict
        :raises FirebaseException
        """
        if data and not isinstance(data, dict):
            raise AttributeError('Data can only be a dict.')
        if notification and not isinstance(notification, dict):
            raise AttributeError('Notification can only be a dict.')
        if not notification and not data:
            raise AttributeError('Data or notification needs to be filled.')
        payload = {'to': to}
        if ttl:
            payload.update({'time_to_live': ttl})
        if data:
            payload.update({'data': data})
        if notification:
            payload.update({'notification': notification})
        return self._request(url=self._http_google_message_api,
                             json_data=payload, headers=self.headers)

    def create_device_group(self, group_name, device_tokens):
        """
        Creates a device group using Google firebase cloud messaging service.
        If device group is created a notification_key for the whole device group
        will be returned, otherwise a FirebaseException will be thrown with
        HTTP status-code and error-message by Google.
        :param group_name:
        :param device_tokens:
        :return: notification_key as string
        :raises FirebaseException
        """
        if not self.sender_id:
            raise ValueError('Sender-ID is required when using device-groups.')
        json_data = self._get_device_group_post_data(operation='create',
                                                device_tokens=device_tokens,
                                                group_name=group_name)
        headers = {'project_id': self.sender_id}
        headers.update(self.headers)
        return self._request(url=self._http_google_notification_api,
                             json_data=json_data, headers=headers)

    def add_device_to_group(self, group_token, device_tokens):
        """
        Adds a device to an existing device-group using the notification_key.
        :param group_token:
        :param device_tokens:
        :return: notification_key as string
        :raises FirebaseException
        """
        if not self.sender_id:
            raise ValueError('Sender-ID is required when using device-groups.')
        json_data = self._get_device_group_post_data(
            operation='add',
            device_tokens=device_tokens,
            group_token=group_token)
        headers = {'project_id': self.sender_id}
        headers.update(self.headers)
        return self._request(url=self._http_google_notification_api,
                             json_data=json_data, headers=headers)

    def remove_device_from_group(self, group_token, device_tokens):
        """
        Remove an existing device from an existing device-group using the
        notification_key of the group.
        :param group_token:
        :param device_tokens:
        :return: notification_key as string
        :raises FirebaseException
        """
        if not self.sender_id:
            raise ValueError('Sender-ID is required when using device-groups.')
        json_data = self._get_device_group_post_data(
            operation='remove',
            device_tokens=device_tokens,
            group_token=group_token)
        headers = {'project_id': self.sender_id}
        headers.update(self.headers)
        return self._request(self._http_google_notification_api,
                             json_data, headers)

    def _request(self, url, json_data, headers):
        resp = requests.post(url=url, json=json_data, headers=headers)
        data = json.loads(resp.text) if resp.text else None
        if data and "error" in data:
            raise FirebaseException(resp.status_code, data['error'])
        elif data and "notification_key" in data:
            return data['notification_key']
        else:
            return data

    def _get_device_group_post_data(self, operation, device_tokens,
                                    group_token=None, group_name=None):
        device_tokens = device_tokens \
            if isinstance(device_tokens, list) else [device_tokens]
        data = {'operation': operation,
                'registration_ids': device_tokens}
        if group_name:
            data.update({'notification_key_name': group_name})
        if group_token:
            data.update({'notification_key': group_token})
        if not group_token and not group_name:
            raise ValueError('No group-token or group-name specified.')
        return data
