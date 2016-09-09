from setuptools import setup

setup(
  name='namespaces',
  version='4.2.0',
  description='Python dictionaries with items also accessible via dot-notation',
  url='https://github.com/pcattori/namespaces',
  author='Pedro Cattori',
  author_email='pcattori@gmail.com',
  license='MIT',
  packages=['namespaces'],
  install_requires=[
    'six>=1.10.0'
  ],
  test_suite='tests'
)
