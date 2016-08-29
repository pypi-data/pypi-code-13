import os
from setuptools import setup, find_packages

import coupons


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-promo',
    version=coupons.__version__,
    description='A reuseable Django application for coupon gereration and handling.',
    long_description=read('README.md'),
    license=read('LICENSE'),
    author='ashwineaso',
    author_email='root@ashwineaso.com',
    url='https://github.com/ashwineaso/django-promo',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
