class FbInput:
    @staticmethod
    def create_text_message(text, quick_reply_payload=None):
        sender_id = 358
        recipient_id = 588667681307355
        message = {
            'seq': 53,
            'mid': 'mid.1466750926480:b2598e311e5ad42d71',
            'text': text
        }
        if quick_reply_payload:
            message.update({
                'quick_reply': {
                    'payload': quick_reply_payload
                }
            })
        template = {
            'sender': {
                'id': sender_id
            },
            'message': message,
            'recipient': {
                'id': recipient_id
            },
            'timestamp': 1466750926487
        }

        return template

    @staticmethod
    def create_attachment_message():
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'mid': 'mid.1466751206432:f290a56f73f8b02b63',
                'seq': 55,
                'sticker_id': 369239263222822,
                'attachments': [{
                    'type': 'image',
                    'payload': {
                        'url': 'https://example.com/image.png'
                    }
                }]
            },
            'timestamp': 1466750926487}

        return template

    @staticmethod
    def create_delivery():
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'delivery': {
                'seq': 12,
                'mids': ['mid.1466675298251:7204294a89a4aae828'],
                'watermark': 1466675298280
            },
            'timestamp': 0}

        return template

    @staticmethod
    def create_postback(payload):
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'postback': {
                'payload': payload
            },
            'timestamp': 1466585047605}

        return template

    @staticmethod
    def create_read():
        template = {
            'read': {
                'watermark': 1467892173172,
                'seq': 537
            },
            'timestamp': 1467892190179,
            'sender': {
                'id': '1129675700423442'
            },
            'recipient': {
                'id': '588667681307355'
            }
        }

        return template

    @staticmethod
    def create_not_supported():
        template = {
            'sender': {
                'id': 1
            },
            'not_supported': {
                'seq': 53,
                'mid': 'mid.1466750926480:b2598e311e5ad42d71',
                'text': 'text'
            },
            'recipient': {
                'id': 1
            },
            'timestamp': 1466750926487}

        return template
