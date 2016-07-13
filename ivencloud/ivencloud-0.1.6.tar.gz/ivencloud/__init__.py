"""
ivencloud is a python library for connecting devices to Iven Cloud.
Checkout the examples folder to see examples.
Further examples and guides can be found in iven blog : http://blog.iven.io

"""


from .api import activate_device, send_data, send_data_wloop, set_frequency, break_sendloop

__title__ = 'ivencloud'
__version__ = '0.1.5'
__author__ = 'Berk Ozdilek'
