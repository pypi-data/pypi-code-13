from setuptools import setup

setup(name='lazy_git',
      version=0.2,
      description='A streamlined REST API for access to Git repositories',
      packages=['lazy_git',
                'lazy_git.api'],
      install_requires=['flask>=0.11.1',
                        'flask-script>=2.0.5',
                        'tornado>=4.3',
                        'sh>=1.11'])
