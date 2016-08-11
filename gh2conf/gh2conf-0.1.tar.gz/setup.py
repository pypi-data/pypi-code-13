from setuptools import setup

version = '0.1'

setup(
    name='gh2conf',
    packages=['gh2conf'],
    version=version,
    description='A script for synchronizing GitHub wiki repositories with Confluence',
    author='Alex Levy',
    author_email='mesozoic@polynode.com',
    url='https://github.com/mesozoic/gh2conf',
    download_url='https://github.com/mesozoic/gh2conf/archive/v{0}.tar.gz'.format(version),
    keywords=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'attrs',
        'markdown',
        'pyyaml',
        'requests',
        'six',
    ],
)
