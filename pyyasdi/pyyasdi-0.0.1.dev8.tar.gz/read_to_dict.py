import logging

import pyYASDI

logging.basicConfig(level=logging.DEBUG)

sma = pyYASDI.pyYASDI(debug=1, max_devices=9)

data = sma.data_all(parameter_channel=False)
