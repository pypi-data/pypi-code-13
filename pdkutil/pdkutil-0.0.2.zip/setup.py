import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pdkutil",
    version='0.0.2',
    author="Simona Iuliana Toader",
    author_email="info@cloudbasesolutions.com",
    description=("Stores a pdk file to a barbican container."),
    license="Apache 2.0",
    keywords="pdk shieldedvms",
    url="https://github.com/cloudbase/pdkutil",
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=['cliff','python-barbicanclient'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Systems Administration'
    ],
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'pdkutil = pdkutil.pdkutil:main'
        ],
        'pdkutil': [
            'store = pdkutil.commands:Store',
            'get = pdkutil.commands:Get',
        ],
    },

    zip_safe=False,
)
