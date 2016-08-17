from setuptools import setup

setup(name='zuoraquery',
      version='0.1',
      description='Query Zuora SOAP API using Zuora Object Query Language (ZOQL)',
      url='https://github.com/michaelperalta/zuoraquery',
      author='Mike Peralta',
      author_email='michaelperalta1@gmail.com',
      license='MIT',
      packages=['zuoraquery'],
      install_requires=[
      'suds',
      ],
      zip_safe=False)