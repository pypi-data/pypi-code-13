import os

devices = []

if os.name == 'nt':
    devices = [
        {'id': 1, 'interface': 'Device\\something1'},
        {'id': 2, 'interface': 'Device\\something2'},
        {'id': 3, 'interface': 'Device\\something3'},
        {'id': 4, 'interface': 'Device\\something4'},
        {'id': 5, 'interface': 'Device\\something5'}
    ]
else:
    devices = [
        {'id': 1, 'interface': 'something1'},
        {'id': 2, 'interface': 'something2'},
        {'id': 3, 'interface': 'something3'},
        {'id': 4, 'interface': 'something4'},
        {'id': 5, 'interface': 'something5'}
    ]

for device in devices:
    print device
