from setuptools import setup

setup(name='openiot',
      version='0.3.1.3',
      description='OpenIoT Gateway',
      url='http://www.openiot.org.ng',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['openiot'],
      scripts=['bin/openiotgw.py'],
      install_requires=[
            'paho-mqtt',
            'configparser',
            'netifaces',
            'pyserial'
      ],
      zip_safe=False)