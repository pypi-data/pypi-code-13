from setuptools import setup

execfile('./cwcli/meta.py')

setup(
    name=__app__,
    packages=[__app__],
    version=__version__,
    description=__description__,
    author=__author__,
    author_email='jacob.bridges.for.hire@gmail.com',
    url='https://github.com/excelmicro/connectwise-soap-cli',
    download_url='https://github.com/excelmicro/connectwise-soap-cli/tarball/{}'.format(
        __version__),
    keywords=['connectwise', 'cli', 'terminal', 'api'],
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'blessings==1.6',
        'click==6.6',
        'pydash==3.4.3',
        'suds==0.4',
        'terminaltables==3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'cw = cwcli.commands.cli',
        ],
    },
)
