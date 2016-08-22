from setuptools import setup

LONG_DESC = open('pypi_readme.rst').read()
LICENSE = open('LICENSE').read()

setup(
    name="giti",
    version="0.0.6",
    description="Command line tool for improve git",
    long_description=LONG_DESC,
    url='http://github.com/xuzhuoyi/giti',
    author='Zhuoyi Xu',
    author_email='xzy476386434@vip.qq.com',
    license=LICENSE,
    packages=["giti"],
    entry_points={
        'console_scripts': [
            'giti=giti.giti:main',
        ]
    },
)
