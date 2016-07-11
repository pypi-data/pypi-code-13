import os

from setuptools import setup, find_packages


VERSION = "?"
execfile(os.path.join(os.path.dirname(__file__),
                      'lovely/essequence/__init__.py'))


requires = [
    'elasticsearch',
]

setup(
    name='lovely.essequence',
    version=VERSION,
    description="a persistent sequence generator for elasticsearch",
    author='lovelysystems',
    author_email='office@lovelysystems.com',
    url='http://github.com/lovelysystems/lovely.essequence',
    packages=find_packages(),
    include_package_data=True,
    extras_require=dict(
        test=[
            'collective.xmltestreport',
            'crate',
            'lovely.testlayers',
        ],
    ),
    zip_safe=False,
    install_requires=requires,
    test_suite="lovely.essequence",
)
