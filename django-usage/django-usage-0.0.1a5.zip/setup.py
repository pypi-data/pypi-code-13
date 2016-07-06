# -*- coding: UTF-8 -*-
"""
    Created by Régis Eduardo Crestani <regis.crestani@gmail.com> on 30/06/2016.
"""
import os

from setuptools import setup, find_packages


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames if not filename.endswith('.pyc')])
    print({package: filepaths})
    return {package: filepaths}


setup(
    name='django-usage',
    version='0.0.1a5',
    description='Django usage reports',
    url='https://github.com/regisec/django-usage/',
    author='Régis Eduardo Crestani',
    author_email='regis.crestani@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['docs', 'test']),
    package_data=get_package_data('django_usage'),
    install_requires=['pygal'],
)
