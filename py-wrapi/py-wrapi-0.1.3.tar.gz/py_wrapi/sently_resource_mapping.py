# coding: utf-8

RESOURCE_MAPPING = {
    'send_sms': {
        'resource': 'api/outboundmessage',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/transactional-message/transactional-message/send-an-sms-using-the-api.',
        'description': "Sends a text message from a specific number to a recipient, all of which must be defined in the request body",
        'methods': 'POST'
    },
    'check_sms': {
        'resource': 'api/outboundmessage/{id}',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/transactional-message/transactional-message/get-the-status-of-a-sent-sms-using-the-api',
        'description': 'Message ID is required',
        'methods': 'GET'
    },
    'all_contacts': {
        'resource': 'api/contacts',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/contacts/list-and-create-contacts/get-a-list-of-all-contacts-in-this-account',
        'description': 'Get a list of all contacts in this account, or update/add contacts depending on HTTP request method',
        'methods': 'GET, POST'
    },
    'contact': {
        'resource': 'api/contacts/{id}',
        'docs': 'http://docs.sentlyweb.apiary.io/#reference/contacts/retrieve-update-or-delete-contacts/get-the-contact-specified-by-the-id',
        'description': 'Message ID is required. Get, update, or delete a specific contact',
        'methods': 'GET, PUT, DELETE'
    }

}

# resp = api.send_sms().post(data=body)()
