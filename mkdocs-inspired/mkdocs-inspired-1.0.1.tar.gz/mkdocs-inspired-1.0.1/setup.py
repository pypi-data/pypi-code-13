"""Setup file to package mkdocs-inspired theme"""
from setuptools import setup, find_packages

VERSION = '1.0.1'


setup(
    name="mkdocs-inspired",
    version=VERSION,
    url='https://github.com/rnason/mkdocs-inspired.git',
    license='MIT',
    description='Mobile responsive Mkdocs theme with slider nav based on bootswatch flatly',
    author='Richard Nason',
    author_email='rich@nason.co',
    packages=find_packages(),
    keywords="pip package, mkdocs, themes",
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'inspired = mkdocs_inspired',
        ]
    },
    zip_safe=False
)
