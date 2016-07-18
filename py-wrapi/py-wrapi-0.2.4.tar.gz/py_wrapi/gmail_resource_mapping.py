# coding: utf-8

RESOURCE_MAPPING = {
    'send_message': {
        'resource': '{email}/messages/send',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/messages/send',
        'methods': ['POST'],
        'remarks': 'To include entire email message in an RFC 2822 formatted and base64url encoded string in request body'
    },
    'message': {
        'resource': '{email}/messages/{message_id}',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/messages/get',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'thread': {
        'resource': '{email}/threads/{thread_id}',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/threads/get',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'all_messages': {
        'resource': '{email}/messages',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/messages/list',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'all_threads': {
        'resource': '{email}/threads',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/threads/list',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'trash_message': {
        'resource': '{email}/messages/{message_id}/trash',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/messages/trash',
        'methods': ['POST'],
        'remarks': 'No request parameters required'
    },
    'trash_thread': {
        'resource': '{email}/threads/{thread_id}/trash',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/threads/trash',
        'methods': ['POST'],
        'remarks': 'No request parameters required'
    },
    'get_self': {
        'resource': '{email}/profile',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/getProfile',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'get_self': {
        'resource': '{email}/labels',
        'docs': 'https://developers.google.com/gmail/api/v1/reference/users/labels/list',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    }

}
