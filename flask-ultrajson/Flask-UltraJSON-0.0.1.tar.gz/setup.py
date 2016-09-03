"""
Flask-UltraJSON
---------------

Intergrates UltraJSON with your Flask application.
"""
from setuptools import setup

setup(
    name='Flask-UltraJSON',
    version='0.0.1',
    url='https://github.com/sunghyunzz/flask-ultrajson',
    license='MIT',
    author='sunghyunzz',
    author_email='me@sunghyunzz.com',
    description='Intergrates UltraJSON with your Flask application.',
    long_description=__doc__,
    py_modules=['flask_ultrajson'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'ujson'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
