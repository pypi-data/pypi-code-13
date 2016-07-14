import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-filebrowser-no-grappelli-staff',
    version='3.6.2.1',
    description='Media Manager sin Grappelli',
    long_description=read('README.rst'),
    url='https://github.com/ccapudev/django-filebrowser-no-grappelli-staff',
    download_url='',
    author='Yelson Chevarrias (ccapudev)',
    author_email='chevarrias@gmail.com',
    maintainer='Yelson Chevarrias',
    maintainer_email='chevarrias@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    zip_safe=True,
)
