from codecs import open
import os.path

from setuptools import setup, find_packages

MY_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(MY_DIR_PATH, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

data_dir_path = os.path.join(MY_DIR_PATH, 'data')
data_files = []
for root_dir_path, _, file_names in os.walk(data_dir_path):
    for file_name in file_names:
        data_files.append(os.path.relpath(os.path.join(root_dir_path, file_name), MY_DIR_PATH))


setup(
    author='Minor Gordon',
    author_email='pastpy@minorgordon.net',
    name='pastpy',
    description='Python library for working with PastPerfect databases',
    license='BSD',
    long_description=long_description,
    url='https://github.com/minorg/pastpy',
    version='1.0.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=('dbf',),

    # What does your project relate to?
    keywords='pastperfect',

    packages=find_packages('src'),
    package_dir = {'':'src'},
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'pastpy.commands.site_template': ['*.mustache'],
    },
)
