import os
import re

import distutils.log

try:
    import setuptools
except ImportError:
    import distutils.core

    setup = distutils.core.setup
else:
    setup = setuptools.setup


PACKAGE = next((str(s) for s in setuptools.find_packages('.', exclude=('tests', 'tests.*'))), None)
PWD = os.path.abspath(os.path.dirname(__file__))
VERSION = (
    re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open(os.path.join(PWD, PACKAGE, '__init__.py')).read())
        .group(1)
)
PYPI_USERNAME = os.environ['PYPI_USERNAME']
PYPI_PASSWORD = os.environ['PYPI_PASSWORD']

with open(os.path.join(PWD, 'README.md')) as f:
    README = f.read()

requires = [
    'coreapi==1.20.0'
]

extras_require = {
    'tests': [
        'nose',
        'coverage'
    ]
}

scripts = [
    # 'bin/citadel'
]


class UploadCommand(distutils.cmd.Command):
    description = 'upload to PyPI'
    user_options = []

    def run(self):
        from twine.commands import upload as twine_upload
        self.announce('running upload %s to PyPI' % str(PACKAGE), level=distutils.log.INFO)
        twine_upload.upload(
            dists=['dist/*'],
            repository='pypi',
            sign=False,
            identity=None,
            username=PYPI_USERNAME,
            password=PYPI_PASSWORD,
            comment=None,
            sign_with='gpg'
        )

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name=PACKAGE,
    version=VERSION,
    description='processing infrastructure',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Very Good',
    author_email='dev@vgs.io',
    license='MIT License',
    packages=[PACKAGE],
    include_package_data=True,
    zip_safe=False,
    scripts=scripts,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    test_suite='nose.collector',
    cmdclass={
        'upload': UploadCommand,
    }
)
