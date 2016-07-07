from setuptools import setup  # Always prefer setuptools over distutils
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='hiveplot',
      long_description='A utility for making hive plots in matplotlib.',
      version='0.1.8.1',
      py_modules=['hiveplot'],
      url='https://github.com/ericmjl/hiveplot',
      author='Eric J. Ma',
      email='ericmajinglong@gmail.com',
      maintainer='Eric J. Ma',
      maintainer_email='ericmajinglong@gmail.com',
      install_requires=reqs,
      )
