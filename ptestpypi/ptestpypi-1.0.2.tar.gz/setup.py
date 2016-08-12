import os
import re
import distutils.log


# try:
#     from semantic_release import setup_hook
#     setup_hook(sys.argv)
# except ImportError as e:
#     print e

try:
    import setuptools
except ImportError:
    import distutils.core
    setup = distutils.core.setup
else:
    setup = setuptools.setup


class PublishCommand(distutils.cmd.Command):
    description = 'deploy to PyPI'
    user_options = []

    def run(self):
        from twine.commands import upload as twine_upload

        self.announce('publish %s: %s' % str(PACKAGE),level=distutils.log.INFO)

        twine_upload.upload(
            dists=['dist/*'],
            repository='pypi',
            sign=False,
            identity=None,
            username="phuonghqh",
            password="SiHill098",
            comment=None,
            sign_with='gpg'
        )
        # command = ['/usr/bin/pylint']
        # if self.pylint_rcfile:
        #     command.append('--rcfile=%s' % self.pylint_rcfile)
        # command.append(os.getcwd())
        # self.announce(
        #     'Running command: %s' % str(command),
        #     level=distutils.log.INFO)
        # subprocess.check_call(command)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


PACKAGE = next((str(s) for s in setuptools.find_packages('.', exclude=('tests', 'tests.*'))), None)

PWD = os.path.abspath(os.path.dirname(__file__))

VERSION = (
    re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open(os.path.join(PWD, PACKAGE, '__init__.py')).read())
        .group(1)
)

with open(os.path.join(PWD, 'README.md')) as f:
    README = f.read()

with open(os.path.join(PWD, 'CHANGES.txt')) as f:
    CHANGES = f.read()

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

setuptools.setup(
    name=PACKAGE,
    version=VERSION,
    description='processing infrastructure',
    long_description=README + '\n\n' + CHANGES,
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
        'publish': PublishCommand,
    }
)

# setup(
#     cmdclass={
#         'pypi': PypiCommand,
#     },
#     name='ptestpypi',
#     version=VERSION,
#     url='https://ptestpypi.com/',
#     license='MIT License',
#     author='ptestpypi',
#     author_email='dev@ptestpypi.com',
#     description='Payments API',
#     long_description=LONG_DESCRIPTION,
#     packages=['ptestpypi'],
#     test_suite='nose.collector',
#     install_requires=parse_requirements('requirements.txt'),
#     tests_require=parse_requirements('test-requirements.txt'),
#     dependency_links=parse_dependency_links('requirements.txt'),
#     classifiers=[
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Topic :: Software Development :: Libraries :: Python Modules',
#     ]
# )
