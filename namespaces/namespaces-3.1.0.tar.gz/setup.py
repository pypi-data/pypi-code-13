from setuptools import setup

setup(
  name='namespaces',
  version='3.1.0',
  description='Python dictionaries with attributes instead of keys',
  url='https://github.com/pcattori/namespaces',
  author='Pedro Cattori',
  author_email='pcattori@gmail.com',
  license='MIT',
  packages=['namespaces'],
  install_requires=[
    'icicle>=0.1.3'
  ]
)
