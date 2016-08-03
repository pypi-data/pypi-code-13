class IPConfig:
    def __init__(self, plugin_name):
        self.data = {
            'General': {
                'Plugin Name': {
                    'Value': plugin_name,
                    'Field Type': 'Label'
                },
                'Flags': {
                    'Value': '/all >>',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Output': {
                    'Value': 'raw',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Extension': {
                    'Values': ['.txt', '.pcap'],
                    'Selected': '.txt',
                    'Field Type': 'Option'
                },
                'Type': {
                    'Values': ['plugin', 'multi', 'schedulable'],
                    'Selected': 'plugin',
                    'Field Type': 'Option'
                },
                'Is Enabled': {
                    'Values': [True, False],
                    'Selected': True,
                    'Field Type': 'Option'
                },
                'Is Standalone': {
                    'Values': [True, False],
                    'Selected': True,
                    'Field Type': 'Option'
                },
                'Parser': {
                    'Value': 'plugins/' + plugin_name + '/parser.py',
                    'Is Path Type': True,
                    'Field Type': 'Entry'
                }
            },
            'Archiving': {
                'File Format': {
                    'Values': ['zip', 'tar'],
                    'Selected': 'tar',
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
                    'Value': '5',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                }
            }
        }
