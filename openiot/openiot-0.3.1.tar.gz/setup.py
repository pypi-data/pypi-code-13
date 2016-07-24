from setuptools import setup

setup(name='openiot',
      version='0.3.1',
      description='OpenIoT Gateway',
      url='http://www.openiot.org.ng',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['openiot'],
      scripts=['bin/openiotgw'],
      zip_safe=False)