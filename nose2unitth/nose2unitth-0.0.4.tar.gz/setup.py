from setuptools import setup, Command
import os


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

version = '0.0.4'

setup(
    name="nose2unitth",
    version=version,
    description="Convert nose-style test reports to UnitTH-style test reports",
    url="https://github.com/KarrLab/nose2unitth",
    download_url='https://github.com/KarrLab/nose2unitth/tarball/%s' % version,
    author="Jonathan Karr",
    author_email="jonrkarr@gmail.com",
    license="MIT",
    keywords='nose unitth xunit junit',
    packages=["nose2unitth"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'nose2unitth = nose2unitth.__main__:main',
        ],
    },
    cmdclass={
        'clean': CleanCommand,
    },
)
