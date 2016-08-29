'''
a redis rpc implementation.
'''

from setuptools import setup


setup(
    name='rrpc',
    version='0.0.2',
    description='a redis rpc implementation',
    long_description=__doc__,
    url='https://github.com/FuGangqiang/rrpc',
    author='FuGangqiang',
    author_email='fu_gangqiang@qq.com',
    keywords='redis rpc json',
    license='MIT',

    py_modules=['rrpc'],
    install_requires=['redis'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)
