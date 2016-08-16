import os
import re

from setuptools import setup

with open('figtree/__init__.py', 'r') as fd:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

REQUIREMENTS = None
if os.path.isfile('requirements.txt'):
    with open('requirements.txt', 'r') as fd:
        REQUIREMENTS = fd.read().splitlines()

EXTRA_KWARGS = {}
if os.environ.get('FIGTREE_NO_LONG_DESCRIPTION', None) is None:
    EXTRA_KWARGS['setup_requires'] = ['setuptools-markdown', ]
    EXTRA_KWARGS['long_description_markdown_filename'] = 'README.md'
else:
    EXTRA_KWARGS['long_description'] = 'None'

setup(
    name='figtree',
    packages=['figtree', ],
    version=VERSION,
    description='Multi-format configuration assembler',
    author='Geoff MacGill',
    author_email='skippydev007@gmail.com',
    url='https://github.com/skippyprime/configs',
    keywords=['config', 'configuration'],
    license='Apache 2.0',
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup'],
    **EXTRA_KWARGS)
