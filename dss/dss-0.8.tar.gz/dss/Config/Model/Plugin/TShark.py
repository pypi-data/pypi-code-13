import os
import subprocess
import csv


class TShark:
    def __init__(self, plugin_name):
        self.data = {
            'General': {
                'Plugin Name': {
                    'Value': plugin_name,
                    'Field Type': 'Label'
                },
                'Flags': {
                    'Value': '-i ' + ' '.join(fetch_ids()) + ' -w',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Output': {
                    'Value': 'raw',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Exe Path': {
                    'Value': 'tshark',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Extension': {
                    'Values': ['.txt', '.pcap'],
                    'Selected': '.pcap',
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
                    'Value': 'plugins.parsers.tshark.tshark_parser,TSharkParser',
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
            },
            'Devices': {
                'Ids': fetch_ids(),
                'Interfaces': fetch_interfaces(),
                'Banned Ids': [],
                'Banned Interfaces': []
            }
        }


def fetch_ids():
    process = subprocess.Popen(['tshark', '-D'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()

    devices = csv.DictReader(stdout.decode('ascii').splitlines(),
                             delimiter=' ', skipinitialspace=True,
                             fieldnames=['id', 'interface'])

    id_array = []

    for device in devices:
        id_array.append(str(device['id'][:-1]))

    return id_array


def fetch_interfaces():
    process = subprocess.Popen(['tshark', '-D'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()

    devices = csv.DictReader(stdout.decode('ascii').splitlines(),
                             delimiter=' ', skipinitialspace=True,
                             fieldnames=['id', 'interface'])

    interface_array = []

    for device in devices:
        interface_array.append(device['interface'])

    return interface_array
