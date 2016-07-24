from setuptools import setup, find_packages

setup(
      install_requires=['distribute', 'Adafruit_MotorHAT>=1.3.0','nxt-python==2.2.2'],
      name = 'drivar',
      description = 'Hardware abstraction layer for Raspbuggy',
      author = 'Brice Copy',
      url = 'https://github.com/cmcrobotics/raspbuggy',
      keywords = ['raspbuggy'],
      version = '0.1.1',
      packages =  find_packages('.')
)
