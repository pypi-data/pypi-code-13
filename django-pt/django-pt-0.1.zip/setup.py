import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-pt',
    version='0.1',
    description='A simple, Django-powered project tracking solution.',
    long_description=read('README.md'),
    url='https://github.com/fstraw/django-pt',
    download_url='',
    author='Brandon Batt',
    author_email='brbatt@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['test_project']),
    include_package_data=True,
    classifiers=[        
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
)