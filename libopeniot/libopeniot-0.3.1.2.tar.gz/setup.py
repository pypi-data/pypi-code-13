from setuptools import setup

setup(name='libopeniot',
      version='0.3.1.2',
      description='OpenIoT Library',
      url='http://www.openiot.org.ng',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['libopeniot'],
      install_requires=[
          'paho-mqtt',
      ],
      zip_safe=False)