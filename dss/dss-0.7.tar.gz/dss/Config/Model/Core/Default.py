class Default:
    def __init__(self):
        self.data = {
            'General': {
                'Parser': {
                    'Value': 'http/parsed/events.json',
                    'Is Path Type': True,
                    'Field Type': 'Entry'
                }
            },
            'Archiving': {
                'File Format': {
                    'Values': ['zip', 'tar'],
                    'Selected': 'zip',
                    'Field Type': 'Option'
                },
                'Archive Size': {
                    'Value': '0',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Size Check Period': {
                    'Value': '0',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Archive Time Interval': {
                    'Value': '7',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                }
            }
        }
