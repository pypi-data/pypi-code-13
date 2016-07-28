"""
Flask-DBKit
-----------

Description goes here...
"""
from setuptools import setup


setup(
    name='Flask-DBKit',
    version='0.0.1',
    url='https://github.com/justinfay/flask-dbkit',
    license='BSD',
    author='Justin Fay',
    author_email='mail@justinfay.me',
    description='dbkit integration for Flask.',
    long_description=__doc__,
    py_modules=['flask_dbkit'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'dbkit'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
