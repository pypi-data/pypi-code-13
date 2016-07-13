# coding: utf-8

RESOURCE_MAPPING = {
    'send_sms': {
        'resource': 'api/outboundmessage',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/transactional-message/transactional-message/send-an-sms-using-the-api.',
        'path_params': None,
        'methods': ['POST'],
        'remarks': 'Request body to contain "from", "to", and "text" fields'
    },
    'check_sms': {
        'resource': 'api/outboundmessage/{message_id}',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/transactional-message/transactional-message/get-the-status-of-a-sent-sms-using-the-api',
        'path_params': ['message_id'],
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'all_contacts': {
        'resource': 'api/contacts',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/contacts/list-and-create-contacts/get-a-list-of-all-contacts-in-this-account',
        'path_params': None,
        'methods': ['GET', 'POST'],
        'remarks': 'For POST requests, refer to docs for request body parameters'
    },
    'contact': {
        'resource': 'api/contacts/{contact_id}',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/contacts/retrieve-update-or-delete-contacts/get-the-contact-specified-by-the-id',
        'path_params': ['contact_id'],
        'methods': ['GET', 'PUT', 'DELETE'],
        'remarks': 'For POST requests, refer to docs for request body parameters'
    }

}
