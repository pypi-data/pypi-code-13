from distutils.core import setup

setup(
    name='autolux',
    version='0.0.8',
    author='okay',
    author_email='okay.zed+kk@gmail.com',
    packages=['autolux' ],
    scripts=['bin/autolux'],
    url='http://github.com/okayzed/autolux',
    license='MIT',
    description='an auto luxer',
    package_data={'': ['README.rst']},
    long_description=open('README.rst').read(),
    )

