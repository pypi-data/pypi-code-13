from setuptools import setup
from setuptools import find_packages

setup(name='mgab-panda',
      version='2.0',
      description='The panda song',
      author='mgab',
      author_email='mgab@panda.com',
      entry_points={
        'console_scripts': [
            'mgabpanda = mgabpanda.__main__:_main',
        ]
      },
      packages=find_packages())
